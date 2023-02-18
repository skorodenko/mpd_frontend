import asyncio
import socket
from mpd.asyncio import MPDClient
from PyQt5.QtCore import QProcess
from ..windows.mpd_socket_config import MpdSocketConfig
from ..constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


class MpdConnector():
    async def _mpd_connect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.mpd_server = QProcess()
            self.mpd_server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
            await asyncio.sleep(0.5)
        
        self.mpd_client = MPDClient()
        await self.mpd_client.connect(socket)
    
    def _mpd_disconnect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.mpd_server.terminate()
            self.mpd_server.waitForFinished(-1)
    
    async def _mpd_connect_dialog(self):
        while True:
            try:
                task = asyncio.create_task(self._mpd_connect(self.config.get("mpd_socket")))
                if not task.done():
                    await task
                e = task.exception()
                self._mpd_idle_task = asyncio.create_task(self._mpd_idle())
                break
            except (socket.gaierror, ConnectionRefusedError):
                if not MpdSocketConfig(self).exec():
                    self.close()
                    break

    async def _media_previous(self):
        await self.mpd_client.previous()
    
    async def _media_next(self):
        await self.mpd_client.next()
    
    async def _media_seeker(self, value):
        await self.mpd_client.seekcur(value)
    
    async def _media_play_pause(self):
        status = await self.mpd_client.status()
        match status["state"]:
            case "stop":
                await self.mpd_client.play(status["song"])
            case "pause":
                await self.mpd_client.pause(0)
            case "play":
                await self.mpd_client.pause(1)
    
    async def _media_repeat(self):
        status = await self.mpd_client.status()
        repeat = status["repeat"]
        single = status["single"]
        match (repeat,single):
            case ("0","0") | ("0","1"):
                await self.mpd_client.repeat(1)
                await self.mpd_client.single(0)
            case ("1","0"):
                await self.mpd_client.repeat(1)
                await self.mpd_client.single(1)
            case ("1","1"):
                await self.mpd_client.repeat(0)
                await self.mpd_client.single(0)
    
    async def _media_shuffle(self):
        status = await self.mpd_client.status()
        shuffle = status["random"]
        match shuffle:
            case "0":
                await self.mpd_client.random(1)
            case "1":
                await self.mpd_client.random(0)