import logging
import qasync
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
        channel = Channel("127.0.0.1", config.default.grpc_port)
        service = TMpdServiceStub(channel)
        status = await service.connect(
            ConnectionCredentials(
                socket = config.default.native_socket
            )
        )
        
        if status.status == ConnectionStatus.Connected:
            self.connected.emit()  
        