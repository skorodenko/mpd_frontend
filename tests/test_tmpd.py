import pytest
import asyncio
import pytest_asyncio
from shutil import which
from unittest.mock import Mock
from src.models import pyd
from src.tmpd import TMPDException, TMPDRequestStatus
from src.models.db import Song, Tile


TABLES = [Song, Tile]


@pytest.mark.asyncio(scope="class")
class TestMPDConnection:
    loop: asyncio.AbstractEventLoop

    @pytest_asyncio.fixture
    async def backend(self):
        from src.tmpd import TMpdBackend

        service = TMpdBackend()
        yield service
        service.close()

    @pytest.mark.skipif(not bool(which("mpd")), reason="No mpd binary found in PATH")
    @pytest.mark.asyncio
    async def test_native_successful_connection(self, backend):
        from src.config import config

        resp = await backend.connect(
            pyd.ConnectionCredentials(
                socket=config.default.native_socket,
                password="",
            )
        )
        assert resp == pyd.ConnectionStatus.Connected

    @pytest.mark.asyncio
    async def test_failed_connection(self, backend):
        resp = await backend.connect(
            pyd.ConnectionCredentials(
                socket="test",
                password="test",
            )
        )
        assert resp == pyd.ConnectionStatus.FailedToConnect


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

    @pytest.fixture(params=[1, 2, 3, 4])
    def tile_limit(self, request, monkeypatch):
        monkeypatch.setattr(
            "src.config.config.prod.tiling_mode", request.param
        )
        return request.param

    @pytest_asyncio.fixture
    async def backend(self):
        from src.tmpd import TMpdBackend

        service = TMpdBackend(mpd_client=self.MockMPDClient())
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
    async def test_db_update(self, backend):
        res = await backend.update_db()
        assert res is None

    @pytest.mark.asyncio
    async def test_list_playlists_empty(self, backend):
        res = await backend.list_playlists()
        assert res == []

    @pytest.mark.asyncio
    async def test_add_tile_invalid_arguments(self, backend):
        with pytest.raises(TMPDException) as e:
            await backend.add_tile(pyd.MetaPlaylist())
        assert e.value.status == TMPDRequestStatus.BAD_REQUEST

    @pytest.mark.asyncio
    async def test_add_tile_valid_arguments(self, backend, tile_limit):
        metas = []
        for _ in range(tile_limit):
            meta = await backend.add_tile(
                pyd.MetaPlaylist(name="Dune", group_by=pyd.SongField.directory)
            )
            metas.insert(0, meta)
        res = await backend.list_playlists()

        assert len(res) == tile_limit
        assert res == metas

    @pytest.mark.asyncio
    async def test_add_tile_cycle(self, backend, tile_limit):
        for i in range(tile_limit + 1):
            tile = await backend.add_tile(
                pyd.MetaPlaylist(name="Dune", group_by=pyd.SongField.directory)
            )
            if i == 0:
                should_be_removed = tile
        res = await backend.list_playlists()

        assert len(res) == tile_limit
        assert should_be_removed not in res

    @pytest.mark.asyncio
    async def test_add_tile_locked_cycle(self, backend, tile_limit):
        for i in range(tile_limit + 1):
            tile = await backend.add_tile(
                pyd.MetaPlaylist(
                    name="Dune", group_by=pyd.SongField.directory, locked=True
                )
            )
            if i == tile_limit:
                not_in_list = tile
        res = await backend.list_playlists()

        assert len(res) == tile_limit
        assert not_in_list not in res

    @pytest.mark.asyncio
    async def test_get_playlist_invalid_playlist(self, backend):
        with pytest.raises(TMPDException) as e:
            await backend.get_playlist(pyd.MetaPlaylist())
        assert e.value.status == TMPDRequestStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_playlist_directory_not_found(self, backend):
        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="not existing directory",
                group_by=pyd.SongField.directory,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
            )
        )
        assert playlist == []

    @pytest.mark.asyncio
    async def test_get_playlist_artist_not_found(self, backend):
        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="not existing artist",
                group_by=pyd.SongField.artist,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
            )
        )
        assert playlist == []

    @pytest.mark.asyncio
    async def test_get_playlist_dir_track_asc(self, backend):
        from tests.data import test_playlist

        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="Dune",
                group_by=pyd.SongField.directory,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
            )
        )
        test_playlist.sort(key=lambda x: int(x["track"]))
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist]
        assert len(playlist) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_dir_track_desc(self, backend):
        from tests.data import test_playlist

        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="Dune",
                group_by=pyd.SongField.directory,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
                sort_order=pyd.SortOrder.Descending,
            )
        )
        test_playlist.sort(key=lambda x: int(x["track"]), reverse=True)
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist]
        assert len(playlist) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_artist_duration_asc(self, backend):
        from tests.data import test_playlist

        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="Hans Zimmer",
                group_by=pyd.SongField.artist,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
                sort_by=pyd.SongField.duration,
            )
        )
        test_playlist.sort(key=lambda x: float(x["duration"]))
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist]
        assert len(playlist) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_get_playlist_artist_duration_desc(self, backend):
        from tests.data import test_playlist

        tile = await backend.add_tile(
            pyd.MetaPlaylist(
                name="Hans Zimmer",
                group_by=pyd.SongField.artist,
            )
        )
        playlist = await backend.get_playlist(
            pyd.MetaPlaylist(
                uuid=tile.uuid,
                sort_by=pyd.SongField.duration,
                sort_order=pyd.SortOrder.Descending,
            )
        )
        test_playlist.sort(key=lambda x: float(x["duration"]), reverse=True)
        true = [f["file"] for f in test_playlist]
        test = [f.file for f in playlist]
        assert len(playlist) == len(test_playlist)
        assert true == test

    @pytest.mark.asyncio
    async def test_delete_tile_invalid_arguments(self, backend):
        with pytest.raises(TMPDException) as e:
            await backend.delete_tile(pyd.MetaPlaylist())
        assert e.value.status == TMPDRequestStatus.BAD_REQUEST

    @pytest.mark.asyncio
    async def test_delete_tile_valid_arguments(self, backend, tile_limit):
        metas = []
        for _ in range(tile_limit):
            meta = await backend.add_tile(
                pyd.MetaPlaylist(name="Dune", group_by=pyd.SongField.directory)
            )
            metas.append(meta)
        for meta in metas:
            await backend.delete_tile(meta)
        res = await backend.list_playlists()

        all_songs = list(Song.select())
        assert res == []
        assert all_songs == []

    @pytest.mark.asyncio
    async def test_toggle_lock_invalid_arguments(self, backend):
        with pytest.raises(TMPDException) as e:
            await backend.toggle_lock(pyd.MetaPlaylist())
        assert e.value.status == TMPDRequestStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_toggle_lock_valid_arguments(self, backend, tile_limit):
        for _ in range(tile_limit):
            meta = await backend.add_tile(
                pyd.MetaPlaylist(name="Dune", group_by=pyd.SongField.directory)
            )
        meta = await backend.toggle_lock(meta)
        res = await backend.list_playlists()

        assert meta.locked is True
        assert res[0] == meta
