import asyncio
from attr import define, field
from mpd.asyncio import MPDClient
from PyQt6.QtCore import QProcess
from soloviy.constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


@define
class MpdConnector:
    main = field()
    client: MPDClient = field(init=False)
    server: QProcess = field(init=False)

    async def mpd_connect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.server = QProcess()
            self.server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
            await asyncio.sleep(0.5)
        
        self.client = MPDClient()
        await self.client.connect(socket)
    
    def mpd_disconnect(self, socket):
        if self.client.connected:
            self.client.clear()
            self.client.disconnect()
        if socket == MPD_NATIVE_SOCKET:
            self.server.terminate()
            self.server.waitForFinished(-1)
    
    async def media_previous(self):
        await self.client.previous()
    
    async def media_next(self):
        await self.client.next()
    
    async def media_seeker(self, value):
        await self.client.seekcur(value)
    
    async def media_play_pause(self):
        status = await self.client.status()
        match status["state"]:
            case "stop":
                await self.client.play(status["song"])
            case "pause":
                await self.client.pause(0)
            case "play":
                await self.client.pause(1)
    
    async def media_repeat(self):
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
    
    async def media_shuffle(self):
        status = await self.client.status()
        shuffle = status["random"]
        match shuffle:
            case "0":
                await self.client.random(1)
            case "1":
                await self.client.random(0)