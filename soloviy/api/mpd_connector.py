import qtinter
import socket
import attrs
import asyncio
import logging
from enum import Enum
from soloviy import db
from soloviy.config import settings
from mpd.asyncio import MPDClient
from PySide6.QtCore import QProcess, Signal, QObject


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
    # Status update is for publishing subsystem: str, status: dict - to update ui components
    update_status: Signal = Signal(str, dict)
    # Seeker update duration: int, elapsed: int
    update_seeker: Signal = Signal(int, int)
    # Emit connection status update
    mpd_connection_status: Signal = Signal(ConnectionStatus)
    # Emit updated playlists tree view
    update_playlists_view: Signal = Signal(list)
    # Emit when fetced playlist to db
    playlist_added: Signal = Signal(str)


@attrs.define
class MpdConnector(QObject, SignalsMixin):
    client: MPDClient = None
    server: QProcess = None
    
    def __attrs_pre_init__(self):
        super().__init__()
        
    def __attrs_post_init__(self):
        self.mpd_connection_status.connect(
            qtinter.asyncslot(self.__publish_playlists)
        )
    
    async def mpd_connect(self, _socket: str):
        logger.info("Connecting to mpd")
        self.mpd_connection_status.emit(ConnectionStatus.CONNECTING)
        if _socket == settings.mpd.native_socket:
            logger.info("Starting native mpd server")
            self.server = QProcess()
            #TODO add check for mpd binary
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
    
    async def playlist_add_db(self, playlist: str):
        await self.client.update()
        data = await self.client.listallinfo(playlist)
        data = [i for i in data if i.get("file")] # Keep files (music) only
        for i, d in enumerate(data, start=0): # Add ids to music 
            d.update({"#": i})
            
        table = db.table(playlist)
        if len(table) > 0:
            db.drop_table(playlist)
        table.insert_multiple(data)
        self.playlist_added.emit(playlist)

    def graceful_close(self):
        # Add idle task cancelation
        if self.client and self.client.connected:
            self.client.clear()
            self.client.disconnect()
        if settings.mpd.socket == settings.mpd.native_socket:
            self.server.terminate()
            self.server.waitForFinished(-1)
            
    async def __publish_playlists(self, status: ConnectionStatus):
        if status == ConnectionStatus.CONNECTED:
            await self.client.update() # TODO Move to another button to update manually
            plsts = await self.client.listfiles(".")           
            self.update_playlists_view.emit(plsts)
            
#    async def __mpd_idle(self):
#        #FIXME Find a way to cancel this task properly
#        #FIXME Restart on disconnect
#        self.client.update()
#        idle_cache = await self.client.status()
#        playlists = await self.client.listfiles(".")
#        await self.cache.set("idle", idle_cache)
#        await self._init_gui(idle_cache, playlists)
#        async for subsys in self.mpd.client.idle():
#            if subsys:
#                new = await self.client.status()
#                idle_cache = await self.cache.get("idle")
#                diff = self.status_diff(idle_cache, new)
#                for d in diff:
#                    self.status_update.emit(d, new)
#                await self.cache.set("idle", new)
#
#    async def __playlist_change(self, index):
#        playlist_name = index.data()
#        playlist = await self.client.listallinfo(playlist_name)
#        self.playlist_publish.emit(playlist)
#    
#    async def __media_previous(self):
#        await self.client.previous()
#    
#    async def __media_next(self):
#        await self.client.next()
#    
#    async def __media_seeker(self, value):
#        await self.client.seekcur(value)
#    
#    async def __media_play_pause(self):
#        status = await self.client.status()
#        match status["state"]:
#            case "stop":
#                await self.client.play(status["song"])
#            case "pause":
#                await self.client.pause(0)
#            case "play":
#                await self.client.pause(1)
#    
#    async def __media_repeat(self):
#        status = await self.client.status()
#        repeat = status["repeat"]
#        single = status["single"]
#        match (repeat,single):
#            case ("0","0") | ("0","1"):
#                await self.client.repeat(1)
#                await self.client.single(0)
#            case ("1","0"):
#                await self.client.repeat(1)
#                await self.client.single(1)
#            case ("1","1"):
#                await self.client.repeat(0)
#                await self.client.single(0)
#    
#    async def __media_shuffle(self):
#        status = await self.client.status()
#        shuffle = status["random"]
#        match shuffle:
#            case "0":
#                await self.client.random(1)
#            case "1":
#                await self.client.random(0)