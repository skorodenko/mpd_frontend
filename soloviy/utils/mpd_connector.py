import asyncio
import socket
from mpd.asyncio import MPDClient
from PyQt5.QtCore import QProcess
from ..widgets.mpd_socket_config import MpdSocketConfig
from ..constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


class MpdConnector:

    def attach_to_main(self, main):
        self.main = main

    async def _mpd_connect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.server = QProcess()
            self.server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
            await asyncio.sleep(0.5)
        
        self.client = MPDClient()
        await self.client.connect(socket)
    
    def _mpd_disconnect(self, socket):
        if self.client.connected:
            self._mpd_idle_task.cancel()
            self.client.clear()
            self.client.disconnect()
        if socket == MPD_NATIVE_SOCKET:
            self.server.terminate()
            self.server.waitForFinished(-1)
    
    async def mpd_connect_dialog(self):
        while True:
            try:
                task = asyncio.create_task(
                    self._mpd_connect(self.main.config.get("mpd_socket"))
                )
                if not task.done():
                    await task
                e = task.exception()
                self._mpd_idle_task = asyncio.create_task(self.main._mpd_idle())
                break
            except (socket.gaierror, ConnectionRefusedError):
                if not MpdSocketConfig(self.main).exec():
                    self.main.close()
                    break

    async def _media_previous(self):
        await self.client.previous()
    
    async def _media_next(self):
        await self.client.next()
    
    async def _media_seeker(self, value):
        await self.client.seekcur(value)
    
    async def _media_play_pause(self):
        status = await self.client.status()
        match status["state"]:
            case "stop":
                await self.client.play(status["song"])
            case "pause":
                await self.client.pause(0)
            case "play":
                await self.client.pause(1)
    
    async def _media_repeat(self):
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
    
    async def _media_shuffle(self):
        status = await self.client.status()
        shuffle = status["random"]
        match shuffle:
            case "0":
                await self.client.random(1)
            case "1":
                await self.client.random(0)