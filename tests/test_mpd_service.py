import time
import pytest
import subprocess
from grpclib.client import Channel
from soloviy.config import settings
from soloviy.backend.protobufs import lib as libgrpc


class TestMPDConnection:
    host = "localhost"
    port = settings.default.grpc_port

    @pytest.fixture
    def grpc_server(self):
        proc = subprocess.Popen(
            ["python", "-m", "soloviy.backend.main"],
            stdout=subprocess.PIPE,
        )

        time.sleep(0.5)
        yield

        proc.terminate()
        time.sleep(0.5)

    @pytest.mark.asyncio
    async def test_native_successful_connection(self, grpc_server):
        channel = Channel(self.host, self.port)
        service = libgrpc.MpdServiceStub(channel)

        resp = await service.connect(
            libgrpc.ConnectionCredentials(
                socket=settings.mpd.native_socket,
                password="",
            )
        )

        channel.close()

        assert resp.status == libgrpc.ConnectionStatus.Connected.value

    @pytest.mark.asyncio
    async def test_failed_connection(self, grpc_server):
        channel = Channel(self.host, self.port)
        service = libgrpc.MpdServiceStub(channel)

        resp = await service.connect(
            libgrpc.ConnectionCredentials(
                socket="test",
                password="test",
            )
        )

        channel.close()

        assert resp.status == libgrpc.ConnectionStatus.FailedToConnect.value
