from datetime import datetime
import attrs
import socket
import logging
import asyncio
import grpclib
from subprocess import Popen
from peewee import DoesNotExist
from pydantic import TypeAdapter
from mpd.asyncio import MPDClient
from soloviy.config import settings
from playhouse.shortcuts import model_to_dict
from soloviy.backend.tmpd import db, models
from betterproto.lib.google.protobuf import Empty
from soloviy.backend.protobufs.lib.tmpd import (
    ListMetaPlaylist,
    TMpdServiceBase,
    ConnectionCredentials,
    ConnectionDetails,
    ConnectionStatus,
    MetaPlaylist,
    Playlist,
    Song,
    SongField,  # noqa: F401
    SortOrder,  # noqa: F401
)


logger = logging.getLogger(__name__)


@attrs.define
class TMpdService(TMpdServiceBase):
    mpd_binary: str | None = attrs.field()
    mpd_server: Popen | None = None
    mpd_client: MPDClient = attrs.Factory(MPDClient)

    @mpd_binary.default
    def _factory_mpd_binary(self) -> bool:
        from shutil import which

        binary = which("mpd")
        if binary:
            logger.debug(f"Found 'mpd' binary: {binary}")
        else:
            logger.debug("Mpd binary not found in PATH")
        return binary

    def close(self):
        logger.debug("Gracefully closing MpdService")
        if self.mpd_client.connected:
            self.mpd_client.disconnect()
        if self.mpd_server:
            self.mpd_server.terminate()
            self.mpd_server.wait(5)

    async def connect(
        self, connection_credentials: ConnectionCredentials
    ) -> ConnectionDetails:
        logger.debug("Establishing connection to mpd")
        if connection_credentials.socket == settings.mpd.native_socket:
            logger.debug("Starting mpd server instance")
            if self.mpd_binary:
                self.mpd_server = Popen(
                    [self.mpd_binary, settings.mpd.native_config, "--no-daemon"]
                )
                await asyncio.sleep(0.5)
            else:
                logger.warning("Mpd binary not found")
                return ConnectionDetails(ConnectionStatus.NoMpdBinary)
        try:
            _socket = connection_credentials.socket
            await self.mpd_client.connect(_socket)
            logger.debug(f"Successfuly connected to mpd: {_socket}")
            return ConnectionDetails(ConnectionStatus.Connected)
        except (socket.gaierror, ConnectionRefusedError):
            logger.warning(f"Failed to connect to mpd: {_socket}")
            return ConnectionDetails(ConnectionStatus.FailedToConnect)

    @property
    def locked_tiles(self) -> int:
        return db.Tile.select().where(db.Tile.locked == True).count()  # noqa: E712

    @property
    def all_tiles(self) -> int:
        return db.Tile.select().count()  # noqa: E712

    @property
    def stacked_tiles(self) -> db.Tile:
        query = db.Tile.select().order_by(-db.Tile.updated, -db.Tile.locked)
        return query

    def _update_tile_db(
        self, meta: models.MetaPlaylistModel, include: list[str] = []
    ) -> models.MetaPlaylistModel:
        tile = db.Tile.get_by_id(meta.uuid)
        tile.update(
            **meta.model_dump(exclude=["uuid", "name", "group_by"], include=include)
        ).execute()
        tile = db.Tile.get_by_id(meta.uuid)
        tile = model_to_dict(tile)
        ta = TypeAdapter(models.MetaPlaylistModel)
        meta = ta.validate_python(tile, from_attributes=True)
        return meta

    async def _get_playlist(self, args: list[str]) -> list[models.SongModel]:
        logger.debug(f"Get (mpd) playlist: '{args}'")
        songs = await self.mpd_client.find(*args)
        if not songs:
            return []
        ta = TypeAdapter(list[models.SongModel])
        songs = ta.validate_python(songs)
        return songs

    async def toggle_lock(self, meta_playlist: MetaPlaylist) -> MetaPlaylist:
        try:
            tile = db.Tile.get_by_id(meta_playlist.uuid)
            tile.locked = not tile.locked
            tile.updated = datetime.now()
            tile.save()
        except DoesNotExist:
            raise grpclib.exceptions.GRPCError(
                grpclib.const.Status.NOT_FOUND,
                f"No playlist with uuid: '{meta_playlist.uuid}'",
            )
        tile = model_to_dict(tile)
        ta_meta = TypeAdapter(MetaPlaylist)
        meta = ta_meta.validate_python(tile, from_attributes=True)
        return meta

    async def list_playlists(
        self, betterproto_lib_google_protobuf_empty: Empty
    ) -> ListMetaPlaylist:
        tiles = list(self.stacked_tiles.dicts())
        ta_list_meta = TypeAdapter(list[MetaPlaylist])
        meta = ta_list_meta.validate_python(tiles, from_attributes=True)
        return ListMetaPlaylist(meta)

    async def get_playlist(self, meta_playlist: MetaPlaylist) -> Playlist:
        meta = models.MetaPlaylistModel.model_validate(meta_playlist)
        try:
            meta = self._update_tile_db(meta, include=["sort_by", "sort_order"])
            songs = meta.db_playlist_query()
        except DoesNotExist:
            raise grpclib.exceptions.GRPCError(
                grpclib.const.Status.NOT_FOUND,
                f"No playlist with uuid: '{meta.uuid}'",
            )
        songs = list(songs.dicts())
        ta_songs = TypeAdapter(list[Song])
        songs = ta_songs.validate_python(songs, from_attributes=True)
        return Playlist(meta=meta_playlist, songs=songs)

    async def add_tile(self, meta_playlist: MetaPlaylist) -> MetaPlaylist:
        meta = models.MetaPlaylistModel.model_validate(meta_playlist)
        try:
            query = meta.mpd_playlist_query()
        except ValueError:
            raise grpclib.exceptions.GRPCError(
                grpclib.const.Status.INVALID_ARGUMENT,
                "Invalid arguments for creating new tile",
            )

        if self.all_tiles == settings.soloviy.tiling_mode:
            if self.locked_tiles < settings.soloviy.tiling_mode:
                tiles = list(self.stacked_tiles)
                poptile = tiles.pop()
                poptile.delete_instance()
            else:
                logger.debug("All tiles are locked")
                return MetaPlaylist()

        songs = await self._get_playlist(query)
        with db.db.atomic():
            tile = db.Tile.create(**meta.model_dump(exclude=["uuid"]))
            for song in songs:
                song = db.Song.create(tile=tile, **song.model_dump())
        logger.debug(f"Added tile: {meta_playlist.name}")

        tile = model_to_dict(tile)
        ta_meta = TypeAdapter(MetaPlaylist)
        meta = ta_meta.validate_python(tile, from_attributes=True)

        return meta

    async def delete_tile(self, meta_playlist: MetaPlaylist) -> MetaPlaylist:
        match meta_playlist.uuid:
            case "":
                raise grpclib.exceptions.GRPCError(
                    grpclib.const.Status.INVALID_ARGUMENT,
                    "Deletion requires 'uuid'",
                )
            case meta_uuid:
                tile = db.Tile.get_by_id(meta_uuid)
                meta = model_to_dict(tile)
                ta_meta = TypeAdapter(MetaPlaylist)
                meta = ta_meta.validate_python(meta, from_attributes=True)
                tile.delete_instance()
        return meta

    async def update_db(self, betterproto_lib_google_protobuf_empty: Empty) -> Empty:
        logger.debug("Started db update")
        await self.mpd_client.update()
        logger.debug("Ended db update")
        return Empty()
