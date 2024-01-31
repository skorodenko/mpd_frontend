import pytest
import asyncio
import grpclib
import pytest_asyncio
from shutil import which
from unittest.mock import Mock
from grpclib.testing import ChannelFor
from src.service.tmpd.db import Song, Tile
from betterproto.lib.google.protobuf import Empty
from src.service.lib import tmpd as libtmpd


TABLES = [Song, Tile]


@pytest.mark.asyncio(scope="class")
class TestMPDConnection:
    loop: asyncio.AbstractEventLoop

    @pytest_asyncio.fixture
    async def grpc_channel(self):
        from src.service.tmpd import TMpdService

        service = TMpdService()
        async with ChannelFor([service]) as channel:
            yield channel
        service.close()

    @pytest.mark.skipif(not bool(which("mpd")), reason="No mpd binary found in PATH")
    @pytest.mark.asyncio
    async def test_native_successful_connection(self, grpc_channel):
        from src.config import config

        service = libtmpd.TMpdServiceStub(grpc_channel)
        resp = await service.connect(
            libtmpd.ConnectionCredentials(
                socket=config.default.native_socket,
                password="",
            )
        )
        assert resp.status == libtmpd.ConnectionStatus.Connected

    @pytest.mark.asyncio
    async def test_failed_connection(self, grpc_channel):
        service = libtmpd.TMpdServiceStub(grpc_channel)
        resp = await service.connect(
            libtmpd.ConnectionCredentials(
                socket="test",
                password="test",
            )
        )
        assert resp.status == libtmpd.ConnectionStatus.FailedToConnect


@pytest.mark.asyncio(scope="class")
class TestMPDDBActions:
    loop: asyncio.AbstractEventLoop

    class MockMPDClient(Mock):
        async def update(self):
            ...

        async def find(self, *args):
            from tests.data import test_playlist

            data = test_playlist
            match args:
                case ["(base 'Dune')", _, _]:
                    data.sort(key=lambda x: int(x["track"]), reverse=True)
                    return data
                case ["(artist == 'Hans Zimmer')", _, _]:
                    data.sort(key=lambda x: float(x["duration"]))
                    return data
        
        async def list(self, *args):
            match args:
                case ["artist"]:
                    return [{"artist": "Hans Zimmer"}, {"artist": ""}]
        
        async def lsinfo(self, *args):
            match args:
                case [""]:
                    return [{"directory": "Dune"}, {"directory": ""}]

    @pytest.fixture(params=[1, 2, 3, 4])
    def tile_limit(self, request, monkeypatch):
        monkeypatch.setattr("src.config.config.prod.tiling_mode", request.param)
        return request.param

    @pytest_asyncio.fixture
    async def grpc_channel(self):
        from src.service.tmpd import TMpdService

        mock_mpd = self.MockMPDClient()
        service = TMpdService(mpd_client=mock_mpd)
        yield service
        service.close()

    @pytest.fixture(autouse=True)
    def mem_db(self):
        from peewee import SqliteDatabase

        db = SqliteDatabase(
            ":memory:",
            pragmas={
                "journal_mode": "wal",
                "foreign_keys": 1,
            },
        )

        db.bind(TABLES, bind_refs=False, bind_backrefs=False)
        db.connect()
        db.create_tables(TABLES)
        yield db
        db.drop_tables(TABLES)
        db.close()

    @pytest.mark.asyncio
    async def test_db_update(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            res = await serv.update_db(Empty())
        assert res == Empty()
        
    @pytest.mark.asyncio
    async def test_list_playlists_artist(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            res = await serv.list_playlists(libtmpd.PlaylistsQuery(
                group=libtmpd.SongField.artist
            ))
        assert res.value == ["Hans Zimmer"]

    @pytest.mark.asyncio
    async def test_list_playlists_directory(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            res = await serv.list_playlists(libtmpd.PlaylistsQuery(
                group=libtmpd.SongField.directory
            ))
        assert res.value == ["Dune"]

    @pytest.mark.asyncio
    async def test_list_tile_empty(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            res = await serv.list_tile(Empty())
        assert res.value == []

    @pytest.mark.asyncio
    async def test_add_tile_invalid_arguments(self, grpc_channel):
        with pytest.raises(grpclib.exceptions.GRPCError) as e:
            async with ChannelFor([grpc_channel]) as channel:
                serv = libtmpd.TMpdServiceStub(channel)
                await serv.add_tile(libtmpd.MetaPlaylist())
        assert e.value.status == grpclib.Status.INVALID_ARGUMENT

    @pytest.mark.asyncio
    async def test_add_tile_valid_arguments(self, grpc_channel, tile_limit):
        metas = []
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            for _ in range(tile_limit):
                meta = await serv.add_tile(
                    libtmpd.MetaPlaylist(
                        name="Dune", group_by=libtmpd.SongField.directory
                    )
                )
                metas.insert(0, meta)
            res = await serv.list_tile(Empty())

        assert len(res.value) == tile_limit
        assert res.value == metas

    @pytest.mark.asyncio
    async def test_add_tile_cycle(self, grpc_channel, tile_limit):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            for i in range(tile_limit + 1):
                tile = await serv.add_tile(
                    libtmpd.MetaPlaylist(
                        name="Dune", group_by=libtmpd.SongField.directory
                    )
                )
                if i == 0:
                    should_be_removed = tile
            res = await serv.list_tile(Empty())

        assert len(res.value) == tile_limit
        assert should_be_removed not in res.value

    @pytest.mark.asyncio
    async def test_add_tile_locked_cycle(self, grpc_channel, tile_limit):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            for i in range(tile_limit + 1):
                tile = await serv.add_tile(
                    libtmpd.MetaPlaylist(
                        name="Dune", group_by=libtmpd.SongField.directory, locked=True
                    )
                )
                if i == tile_limit:
                    not_in_list = tile
            res = await serv.list_tile(Empty())

        assert len(res.value) == tile_limit
        assert not_in_list not in res.value

    @pytest.mark.asyncio
    async def test_get_playlist_invalid_playlist(self, grpc_channel):
        with pytest.raises(grpclib.exceptions.GRPCError) as e:
            async with ChannelFor([grpc_channel]) as channel:
                serv = libtmpd.TMpdServiceStub(channel)
                await serv.get_playlist(libtmpd.MetaPlaylist())
        assert e.value.status == grpclib.Status.NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_playlist_directory_not_found(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="not existing directory",
                    group_by=libtmpd.SongField.directory,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                )
            )
        assert tile.uuid == playlist.meta.uuid
        assert playlist.songs == []

    @pytest.mark.asyncio
    async def test_get_playlist_artist_not_found(self, grpc_channel):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="not existing artist",
                    group_by=libtmpd.SongField.artist,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                )
            )
        assert tile.uuid == playlist.meta.uuid
        assert playlist.songs == []

    @pytest.mark.asyncio
    async def test_get_playlist_dir_track_asc(self, grpc_channel):
        from tests.data import test_playlist

        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="Dune",
                    group_by=libtmpd.SongField.directory,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                )
            )
        test_playlist.sort(key=lambda x: int(x["track"]))
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist.songs]
        assert tile.uuid == playlist.meta.uuid
        assert len(playlist.songs) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_dir_track_desc(self, grpc_channel):
        from tests.data import test_playlist

        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="Dune",
                    group_by=libtmpd.SongField.directory,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                    sort_order=libtmpd.SortOrder.Descending,
                )
            )
        test_playlist.sort(key=lambda x: int(x["track"]), reverse=True)
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist.songs]
        assert tile.uuid == playlist.meta.uuid
        assert len(playlist.songs) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_artist_duration_asc(self, grpc_channel):
        from tests.data import test_playlist

        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="Hans Zimmer",
                    group_by=libtmpd.SongField.artist,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                    sort_by=libtmpd.SongField.duration,
                )
            )
        test_playlist.sort(key=lambda x: float(x["duration"]))
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist.songs]
        assert tile.uuid == playlist.meta.uuid
        assert len(playlist.songs) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_artist_duration_desc(self, grpc_channel):
        from tests.data import test_playlist

        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            tile = await serv.add_tile(
                libtmpd.MetaPlaylist(
                    name="Hans Zimmer",
                    group_by=libtmpd.SongField.artist,
                )
            )
            playlist = await serv.get_playlist(
                libtmpd.MetaPlaylist(
                    uuid=tile.uuid,
                    sort_by=libtmpd.SongField.duration,
                    sort_order=libtmpd.SortOrder.Descending,
                )
            )
        test_playlist.sort(key=lambda x: float(x["duration"]), reverse=True)
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist.songs]
        print(true)
        print(test)
        assert tile.uuid == playlist.meta.uuid
        assert len(playlist.songs) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_delete_tile_invalid_arguments(self, grpc_channel):
        with pytest.raises(grpclib.exceptions.GRPCError) as e:
            async with ChannelFor([grpc_channel]) as channel:
                serv = libtmpd.TMpdServiceStub(channel)
                await serv.delete_tile(libtmpd.MetaPlaylist())
        assert e.value.status == grpclib.Status.INVALID_ARGUMENT

    @pytest.mark.asyncio
    async def test_delete_tile_valid_arguments(self, grpc_channel, tile_limit):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            metas = []
            for _ in range(tile_limit):
                meta = await serv.add_tile(
                    libtmpd.MetaPlaylist(
                        name="Dune", group_by=libtmpd.SongField.directory
                    )
                )
                metas.append(meta)
            for meta in metas:
                await serv.delete_tile(meta)
            res = await serv.list_tile(Empty())

        all_songs = list(Song.select())
        assert res.value == []
        assert all_songs == []

    @pytest.mark.asyncio
    async def test_toggle_lock_invalid_arguments(self, grpc_channel):
        with pytest.raises(grpclib.exceptions.GRPCError) as e:
            async with ChannelFor([grpc_channel]) as channel:
                serv = libtmpd.TMpdServiceStub(channel)
                await serv.toggle_lock(libtmpd.MetaPlaylist())
        assert e.value.status == grpclib.Status.NOT_FOUND

    @pytest.mark.asyncio
    async def test_toggle_lock_valid_arguments(self, grpc_channel, tile_limit):
        async with ChannelFor([grpc_channel]) as channel:
            serv = libtmpd.TMpdServiceStub(channel)
            for _ in range(tile_limit):
                meta = await serv.add_tile(
                    libtmpd.MetaPlaylist(
                        name="Dune", group_by=libtmpd.SongField.directory
                    )
                )
            meta = await serv.toggle_lock(meta)
            res = await serv.list_tile(Empty())

        assert meta.locked is True
        assert res.value[0] == meta
