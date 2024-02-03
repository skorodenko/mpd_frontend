import qasync
import asyncio
import logging
from PySide6.QtCore import QObject, Signal
from PySide6.QtQml import QmlElement, QmlSingleton
from grpclib.client import Channel
from src.config import config
from src.service.lib.tmpd import TMpdServiceStub, ConnectionCredentials, ConnectionStatus


logger = logging.getLogger(__name__)

QML_IMPORT_NAME = "controllers"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0 # Optional


@QmlElement
@QmlSingleton
class Main(QObject):
    connected: Signal = Signal()
    
    def __init__(self):
        super().__init__()
    
    @qasync.asyncSlot()
    async def connect(self):
        SLEEP_TIME = 10
        for _ in range(SLEEP_TIME * 4):
            try:
                channel = Channel(path=config.default.grpc_host)
                service = TMpdServiceStub(channel)
                status = await service.connect(
                    ConnectionCredentials(
                        socket = config.default.native_socket
                    )
                )
                if status == ConnectionStatus.FailedToConnect:
                    continue
                break
            except ConnectionRefusedError:
                await asyncio.sleep(0.25)
        
        if status.status == ConnectionStatus.Connected:
            self.connected.emit()  
        