import qtinter
import socket
import attrs
import asyncio
from typing import Coroutine
from mpd.asyncio import MPDClient
from aiocache import Cache
from PyQt6.QtCore import QProcess, QObject, pyqtSignal
from soloviy.widgets.mpd_socket_config import MpdSocketConfig
from soloviy.constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


@attrs.define
class MpdConnector(QObject):
    client: MPDClient = attrs.field(init=False)
    server: QProcess = attrs.field(init=False)
    cache: Cache = attrs.Factory(Cache)
    
    mpd_connect: pyqtSignal = pyqtSignal(str)
    mpd_disconnect: pyqtSignal = pyqtSignal(str)
    mpd_idle_task: Coroutine = None
    
    # Status update is for publishing subsystem: str, status: dict - to update ui components
    status_update: pyqtSignal = pyqtSignal(str, dict)
    
    #playlist_clear: pyqtSignal = pyqtSignal()
    playlist_change: pyqtSignal = pyqtSignal(str)
    #playlist_publish: pyqtSignal = pyqtSignal(list[dict])
    
    def __attrs_pre_init__(self):
        super().__init__()
    
    def __attrs_post_init__(self):
        #self.mpd_connect.connect(qtinter.asyncslot(self.__mpd_connect_dialog))
        #self.mpd_disconnect.connect(qtinter.asyncslot(self.__mpd_disconnect))
##        self.media_previous.connect(qtinter.asyncslot(self.__media_previous))
##        self.media_next.connect(qtinter.asyncslot(self.__media_next))
##        self.media_seeker.connect(qtinter.asyncslot(self.__media_seeker))
##        self.media_play_pause.connect(qtinter.asyncslot(self.__media_play_pause))
##        self.media_repeat.connect(qtinter.asyncslot(self.__media_repeat))
##        self.media_shuffle.connect(qtinter.asyncslot(self.__media_shuffle))
        #self.playlist_change.connect(qtinter.asyncslot(self.__playlist_change))
        ...
    
    @staticmethod
    def status_diff(old, new):
        return [k for k in old.keys() 
            if old.get(k) != new.get(k)
            and old.get(k) is not None
            and new.get(k) is not None]
    
    async def __mpd_connect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.server = QProcess()
            self.server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
            await asyncio.sleep(0.5)
        
        self.client = MPDClient()
        await self.client.connect(socket)
    
    async def __mpd_connect_dialog(self):
        while True:
            try:
                task = asyncio.create_task(
                    self.__mpd_connect(MPD_NATIVE_SOCKET)
                )
                if not task.done():
                    await task
                task.exception()
                self.mpd_idle_task = asyncio.create_task(self.__mpd_idle())
                break
            except (socket.gaierror, ConnectionRefusedError):
                if not MpdSocketConfig(self).exec():
                    self.close()
                    break
    
    async def __mpd_disconnect(self, socket):
        if self.client.connected:
            self.client.clear()
            self.client.disconnect()
        if socket == MPD_NATIVE_SOCKET:
            self.server.terminate()
            self.server.waitForFinished(-1)

    async def __mpd_idle(self):
        #FIXME Find a way to cancel this task properly
        #FIXME Restart on disconnect
        self.client.update()
        idle_cache = await self.client.status()
        playlists = await self.client.listfiles(".")
        await self.cache.set("idle", idle_cache)
        await self._init_gui(idle_cache, playlists)
        async for subsys in self.mpd.client.idle():
            if subsys:
                new = await self.client.status()
                idle_cache = await self.cache.get("idle")
                diff = self.status_diff(idle_cache, new)
                for d in diff:
                    self.status_update.emit(d, new)
                await self.cache.set("idle", new)

    async def __playlist_change(self, index):
        playlist_name = index.data()
        playlist = await self.client.listallinfo(playlist_name)
        self.playlist_publish.emit(playlist)
    
    async def __media_previous(self):
        await self.client.previous()
    
    async def __media_next(self):
        await self.client.next()
    
    async def __media_seeker(self, value):
        await self.client.seekcur(value)
    
    async def __media_play_pause(self):
        status = await self.client.status()
        match status["state"]:
            case "stop":
                await self.client.play(status["song"])
            case "pause":
                await self.client.pause(0)
            case "play":
                await self.client.pause(1)
    
    async def __media_repeat(self):
        status = await self.client.status()
        repeat = status["repeat"]
        single = status["single"]
        match (repeat,single):
            case ("0","0") | ("0","1"):
                await self.client.repeat(1)
                await self.client.single(0)
            case ("1","0"):
                await self.client.repeat(1)
                await self.client.single(1)
            case ("1","1"):
                await self.client.repeat(0)
                await self.client.single(0)
    
    async def __media_shuffle(self):
        status = await self.client.status()
        shuffle = status["random"]
        match shuffle:
            case "0":
                await self.client.random(1)
            case "1":
                await self.client.random(0)