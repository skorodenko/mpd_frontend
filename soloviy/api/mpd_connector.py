import qtinter
import socket
import attrs
import asyncio
import logging
from enum import Enum
from typing import List
from pydantic import TypeAdapter
from mpd.asyncio import MPDClient
from soloviy.config import settings
from soloviy.models import dbmodels as db
from soloviy.models import pydanticmodels as pmodels
from PySide6.QtCore import QProcess, Signal, QObject, Slot


logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """Connection status update"""
    CONNECTED = 1
    CONNECTING = 2
    DISCONNECTED = 3
    CONNECTION_LOST = 4
    CONNECTION_TIMEOUT = 5
    CONNECTION_FAILED = 6


class SignalsMixin:
    # Status update is for publishing subsystem, status - to update ui components
    update_status: Signal = Signal(str, dict)
    # Seeker update duration: int, elapsed: int
    update_seeker: Signal = Signal(int, int)
    # Emit connection status update
    mpd_connection_status: Signal = Signal(ConnectionStatus)
    # Emit when fetced playlist to db
    playlist_populated: Signal = Signal(str) # DEPRECETAED
    # Emit when db updated finished
    db_updated: Signal = Signal()


@attrs.define
class MpdConnector(QObject, SignalsMixin):
    client: MPDClient = None
    server: QProcess = None
    
    def __attrs_pre_init__(self):
        super().__init__()
        
    def __attrs_post_init__(self):
        ...
    
    async def mpd_connect(self, _socket: str):
        logger.info("Connecting to mpd")
        self.mpd_connection_status.emit(ConnectionStatus.CONNECTING)
        if _socket == settings.mpd.native_socket:
            logger.info("Starting native mpd server")
            self.server = QProcess()
            self.server.start("mpd", [settings.mpd.native_config, "--no-daemon"])
            await asyncio.sleep(0.5)
        try:
            self.client = MPDClient()
            await self.client.connect(_socket)
            logger.info("Successfuly connected to mpd")
            self.mpd_connection_status.emit(ConnectionStatus.CONNECTED)
        except (socket.gaierror, ConnectionRefusedError):
            logger.warning("Failed to connect to mpd")
            self.mpd_connection_status.emit(ConnectionStatus.CONNECTION_FAILED)
            
    @staticmethod
    def group_by_folders(data: list[dict]) -> dict[list[dict]]:
        res = dict()
        for item in data:
            if directory := item.get("directory"):
                res[directory] = []
                partial_res = res[directory]
                continue
            partial_res.append(item)
        return res
    
    @Slot()
    async def update_db(self):
        logger.debug("Started db update")
        await self.client.update()
        data = await self.client.listallinfo()
        data = self.group_by_folders(data)
        for directory in data:
            ta = TypeAdapter(List[pmodels.Library])
            sdata = data[directory]
            sdata = [i for i in sdata if i.get("file")]
            sdata = ta.validate_python(sdata, context={"directory": directory})
            sdata = ta.dump_python(sdata)
            db.Library.insert_many(sdata).execute()
        logger.debug("Ended db update")
        self.db_updated.emit()

    def graceful_close(self):
        # Add idle task cancelation
        if self.client and self.client.connected:
            self.client.clear()
            self.client.disconnect()
        if settings.mpd.socket == settings.mpd.native_socket:
            self.server.terminate()
            self.server.waitForFinished(-1)
            