import time
import pytest
import subprocess
from grpclib.client import Channel
from soloviy.config import settings
from soloviy.backend.protobufs import lib as libgrpc



@pytest.fixture
def grpc_server():
    proc = subprocess.Popen(
        ["python", "-m", "soloviy.backend.main"],
        stdout=subprocess.PIPE,
    )
    
    time.sleep(0.5)
    yield
    
    proc.terminate()
    time.sleep(0.5)


@pytest.mark.asyncio
async def test_native_successful_connection(grpc_server):
    channel = Channel("localhost", 50051)
    service = libgrpc.MpdServiceStub(channel)
    
    resp = await service.connect(
        libgrpc.ConnectionCredentials(
            socket = settings.mpd.native_socket, 
            password = "",
        )
    )
    
    channel.close()
    
    assert resp.status == libgrpc.ConnectionStatus.Connected.value
    


@pytest.mark.asyncio
async def test_failed_connection(grpc_server):
    channel = Channel("localhost", 50051)
    service = libgrpc.MpdServiceStub(channel)
    
    resp = await service.connect(
        libgrpc.ConnectionCredentials(
            socket = "test", 
            password = "test",
        )
    )
    
    channel.close()
    
    assert resp.status == libgrpc.ConnectionStatus.FailedToConnect.value