import pytest
import asyncio
import pytest_asyncio
from shutil import which
from unittest.mock import Mock
from peewee import SqliteDatabase
from grpclib.testing import ChannelFor
from betterproto.lib.google.protobuf import Empty
from soloviy.backend.services.mpd import MpdService
from soloviy.backend.protobufs import lib as libgrpc


@pytest.mark.asyncio(scope="class")
class TestMPDConnection:
    loop: asyncio.AbstractEventLoop

    @pytest_asyncio.fixture
    async def grpc_channel(self):
        service = MpdService()
        async with ChannelFor([service]) as channel:
            yield channel
        service.close()

    @pytest.mark.skipif(not bool(which("mpd")), reason="No mpd binary found in PATH")
    @pytest.mark.asyncio
    async def test_native_successful_connection(self, grpc_channel):
        from soloviy.config import settings

        service = libgrpc.MpdServiceStub(grpc_channel)

        resp = await service.connect(
            libgrpc.ConnectionCredentials(
                socket=settings.mpd.native_socket,
                password="",
            )
        )

        assert resp.status == libgrpc.ConnectionStatus.Connected.value

    @pytest.mark.asyncio
    async def test_failed_connection(self, grpc_channel):
        service = libgrpc.MpdServiceStub(grpc_channel)

        resp = await service.connect(
            libgrpc.ConnectionCredentials(
                socket="test",
                password="test",
            )
        )

        assert resp.status == libgrpc.ConnectionStatus.FailedToConnect.value


@pytest.mark.asyncio(scope="class")
class TestMPDAppDB:
    loop: asyncio.AbstractEventLoop

    class MockMPDClient(Mock):
        async def update(self):
            ...

        async def listallinfo(self):
            res = [
                {
                    "directory": "testdir",
                    "last-modified": "2023-07-13T15:13:40Z",
                },
                {
                    "file": "testdir/song1.mp3",
                    "last-modified": "2023-07-13T15:13:40Z",
                    "format": "44100:24:2",
                    "artist": ["artist1", "artist2"],
                    "albumartist": "artist1",
                    "title": "song1",
                    "album": "album1",
                    "track": "1",
                    "date": "2023",
                    "genre": "Test Music",
                    "disc": "1",
                    "time": "291",
                    "duration": "290.899",
                },
                {
                    "file": "testdir/song2.mp3",
                    "last-modified": "2023-07-13T15:13:40Z",
                    "format": "44100:24:2",
                    "artist": ["artist1", "artist2"],
                    "albumartist": "artist1",
                    "title": "song2",
                    "album": "album1",
                    "track": "2",
                    "date": "2023",
                    "genre": ["Test Music 1", "Test Music 2"],
                    "disc": "1",
                    "time": "291",
                    "duration": "290.899",
                },
            ]
            return res

    @pytest.fixture
    def mem_db(self, monkeypatch):
        db = SqliteDatabase(
            ":memory:",
            pragmas={
                "journal_mode": "wal",
            },
        )
        monkeypatch.setattr("soloviy.backend.services.mpd.db.db", db)
        yield db
        db.close()

    @pytest_asyncio.fixture
    async def grpc_channel(self):
        service = MpdService(mpd_client=self.MockMPDClient())
        async with ChannelFor([service]) as channel:
            yield channel
        service.close()

    @pytest.mark.asyncio
    async def test_db_update(self, mem_db, grpc_channel):
        from soloviy.backend.services.mpd.db import Library

        service = libgrpc.MpdServiceStub(grpc_channel)

        await service.update_db(Empty())

        record = Library.get(Library.title == "song1")

        assert bool(record)

    @pytest.mark.asyncio
    async def test_composite_metadata(self, mem_db, grpc_channel):
        from soloviy.backend.services.mpd.db import Library

        service = libgrpc.MpdServiceStub(grpc_channel)

        await service.update_db(Empty())

        record = Library.get(Library.title == "song2")

        assert record.artist == "artist1,artist2"
