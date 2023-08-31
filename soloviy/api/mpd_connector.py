import qtinter
import socket
import attrs
import asyncio
from enum import Enum
from soloviy.config import settings
from typing import Coroutine
from mpd.asyncio import MPDClient
from PySide6.QtCore import QProcess, Signal, QObject


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
    
    mpd_connection_status: Signal = Signal(ConnectionStatus)
    

@attrs.define
class MpdConnector(QObject, SignalsMixin):
    client: MPDClient = None
    server: QProcess = None
    
    def __attrs_pre_init__(self):
        super().__init__()
    
    @staticmethod
    def status_diff(old, new):
        return [k for k in old.keys() 
            if old.get(k) != new.get(k)
            and old.get(k) is not None
            and new.get(k) is not None]
    
    async def mpd_connect(self, _socket):
        self.mpd_connection_status.emit(ConnectionStatus.CONNECTING)
        if _socket == settings.mpd.native_socket:
            self.server = QProcess()
            self.server.start("mpd", [settings.mpd.native_config, "--no-daemon"])
            await asyncio.sleep(0.5)
        try:
            self.client = MPDClient()
            await self.client.connect(_socket)
            self.mpd_connection_status.emit(ConnectionStatus.CONNECTED)
        except (socket.gaierror, ConnectionRefusedError):
            self.mpd_connection_status.emit(ConnectionStatus.CONNECTION_FAILED)

    def graceful_close(self):
        # Add idle task
        if self.client and self.client.connected:
            self.client.clear()
            self.client.disconnect()
        if settings.mpd.socket == settings.mpd.native_socket:
            self.server.terminate()
            self.server.waitForFinished(-1)

    
#    async def __mpd_connect_dialog(self):
#        while True:
#            try:
#                task = asyncio.create_task(
#                    self.__mpd_connect(MPD_NATIVE_SOCKET)
#                )
#                if not task.done():
#                    await task
#                task.exception()
#                self.mpd_idle_task = asyncio.create_task(self.__mpd_idle())
#                break
#            except (socket.gaierror, ConnectionRefusedError):
#                if not MpdSocketConfig(self).exec():
#                    self.close()
#                    break
#    
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