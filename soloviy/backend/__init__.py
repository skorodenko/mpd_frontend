import socket
import logging
import asyncio
from dataclasses import dataclass, field
from PySide6.QtCore import QObject, QProcess
from datetime import datetime
from peewee import DoesNotExist
from pydantic import TypeAdapter
from mpd.asyncio import MPDClient
from playhouse.shortcuts import model_to_dict
from soloviy.backend import db
from soloviy.config import settings
from soloviy.backend import exceptions, utils
from soloviy.backend.models import (
    ConnectionCredentials,
    ConnectionStatus,
    MetaPlaylist,
    Song,
    SongField,  # noqa: F401
    SortOrder,  # noqa: F401
)


logger = logging.getLogger(__name__)


@dataclass
class TMpdBackend(QObject):
    mpd_binary: str | None = field(default_factory=utils.factory_mpd_binary)
    mpd_server: QProcess = field(default_factory=QProcess)
    mpd_client: MPDClient = field(default_factory=MPDClient)

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

    async def connect(
        self, connection_credentials: ConnectionCredentials
    ) -> ConnectionStatus:
        logger.debug("Establishing connection to mpd")
        if connection_credentials.socket == settings.default.native_socket:
            logger.debug("Starting mpd server instance")
            if self.mpd_binary:
                self.mpd_server.start(
                    self.mpd_binary, [settings.default.native_config, "--no-daemon"]
                )
                await asyncio.sleep(0.5)
            else:
                logger.warning("Mpd binary not found")
                return ConnectionStatus.NoMpdBinary
        try:
            _socket = connection_credentials.socket
            await self.mpd_client.connect(_socket)
            logger.debug(f"Successfuly connected to mpd: {_socket}")
            return ConnectionStatus.Connected
        except (socket.gaierror, ConnectionRefusedError):
            logger.warning(f"Failed to connect to mpd: {_socket}")
            return ConnectionStatus.FailedToConnect

    def close(self):
        logger.debug("Gracefully closing MpdService")
        if self.mpd_client.connected:
            self.mpd_client.disconnect()
        if self.mpd_server:
            self.mpd_server.terminate()
            self.mpd_server.waitForFinished(5000)

    def _update_tile_db(
        self, meta: MetaPlaylist, include: list[str] = []
    ) -> MetaPlaylist:
        tile = db.Tile.get_by_id(meta.uuid)
        tile.update(
            **meta.model_dump(exclude=["uuid", "name", "group_by"], include=include)
        ).execute()
        tile = db.Tile.get_by_id(meta.uuid)
        tile = model_to_dict(tile)
        ta = TypeAdapter(MetaPlaylist)
        meta = ta.validate_python(tile, from_attributes=True)
        return meta

    async def _get_playlist(self, args: list[str]) -> list[Song]:
        logger.debug(f"Get (mpd) playlist: '{args}'")
        songs = await self.mpd_client.find(*args)
        if not songs:
            return []
        ta = TypeAdapter(list[Song])
        songs = ta.validate_python(songs)
        return songs

    async def toggle_lock(self, meta: MetaPlaylist) -> MetaPlaylist:
        try:
            tile = db.Tile.get_by_id(meta.uuid)
            tile.locked = not tile.locked
            tile.updated = datetime.now()
            tile.save()
        except DoesNotExist:
            raise exceptions.TMPDException(
                exceptions.Status.NOT_FOUND,
                f"No playlist with uuid: '{meta.uuid}'",
            )
        tile = model_to_dict(tile)
        ta_meta = TypeAdapter(MetaPlaylist)
        meta = ta_meta.validate_python(tile, from_attributes=True)
        return meta

    async def list_playlists(self) -> list[MetaPlaylist]:
        tiles = list(self.stacked_tiles.dicts())
        ta_list_meta = TypeAdapter(list[MetaPlaylist])
        list_meta = ta_list_meta.validate_python(tiles, from_attributes=True)
        return list_meta

    async def get_playlist(self, meta: MetaPlaylist) -> list[Song]:
        try:
            meta = self._update_tile_db(meta, include=["sort_by", "sort_order"])
            songs = meta.db_playlist_query()
        except DoesNotExist:
            raise exceptions.TMPDException(
                exceptions.Status.NOT_FOUND, f"No playlist with uuid: '{meta.uuid}'"
            )
        songs = list(songs.dicts())
        ta_songs = TypeAdapter(list[Song])
        songs = ta_songs.validate_python(songs, from_attributes=True)
        return songs

    async def add_tile(self, meta: MetaPlaylist) -> MetaPlaylist:
        try:
            query = meta.mpd_playlist_query()
        except ValueError:
            raise exceptions.TMPDException(
                exceptions.Status.BAD_REQUEST,
                "Invalid arguments for creating new tile",
            )

        if self.all_tiles == settings.prod.tiling_mode:
            if self.locked_tiles < settings.prod.tiling_mode:
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
        logger.debug(f"Added tile: {meta.name}")

        tile = model_to_dict(tile)
        ta_meta = TypeAdapter(MetaPlaylist)
        meta = ta_meta.validate_python(tile, from_attributes=True)

        return meta

    async def delete_tile(self, meta_playlist: MetaPlaylist) -> MetaPlaylist:
        match meta_playlist.uuid:
            case None:
                raise exceptions.TMPDException(
                    exceptions.Status.BAD_REQUEST,
                    "Deletion requires 'uuid'",
                )
            case meta_uuid:
                tile = db.Tile.get_by_id(meta_uuid)
                meta = model_to_dict(tile)
                ta_meta = TypeAdapter(MetaPlaylist)
                meta = ta_meta.validate_python(meta, from_attributes=True)
                tile.delete_instance()
        return meta

    async def update_db(self) -> None:
        logger.debug("Started db update")
        await self.mpd_client.update()
        logger.debug("Ended db update")
