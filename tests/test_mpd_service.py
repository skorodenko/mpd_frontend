import pytest
import asyncio
import pytest_asyncio
from shutil import which
from grpclib.testing import ChannelFor
from soloviy.backend.services.mpd import MpdService
from soloviy.backend.protobufs import lib as libgrpc
from soloviy.config import settings


@pytest.mark.asyncio(scope="class")
class TestMPDConnection:
    host = "localhost"
    port = settings.default.grpc_port
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
