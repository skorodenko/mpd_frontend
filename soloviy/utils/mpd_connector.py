import time
import asyncio
from mpd import MPDClient
from PyQt6.QtCore import QProcess
from ..windows.mpd_socket_config import MpdSocketConfig
from ..constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


class MpdConnector():
    def _mpd_connect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.mpd_server = QProcess()
            self.mpd_server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
            time.sleep(0.5)
        
        self.mpd_client = MPDClient()
        self.mpd_client.connect(socket)
    
    def _mpd_disconnect(self, socket):
        if socket == MPD_NATIVE_SOCKET:
            self.mpd_server.terminate()
            self.mpd_server.waitForFinished(-1)
        self.mpd_client.disconnect()
    
    def _mpd_connect_dialog(self):
        while True:
            try:
                self._mpd_connect(self.config.get("mpd_socket"))
                self._mpd_idle_task = asyncio.create_task(self._mpd_idle(self.config.get("mpd_socket")))
                break
            except (ConnectionRefusedError, AttributeError, ValueError):
                if not MpdSocketConfig(self).exec():
                    self.close()
                    break
    
    def _media_previous(self):
        self.mpd_client.previous()
    
    def _media_next(self):
        self.mpd_client.next()
    
    def _media_seeker(self, value):
        if value:
            self.mpd_client.seekcur(value)
    
    def _media_play_pause(self):
        match self.mpd_client.status()["state"]:
            case "pause" | "stop":
                self.mpd_client.pause(0)
            case "play":
                self.mpd_client.pause(1)
    
    def _media_repeat(self):
        status = self.mpd_client.status()
        repeat = status["repeat"]
        single = status["single"]
        match (repeat,single):
            case ("0","0") | ("0","1"):
                self.mpd_client.repeat(1)
                self.mpd_client.single(0)
            case ("1","0"):
                self.mpd_client.repeat(1)
                self.mpd_client.single(1)
            case ("1","1"):
                self.mpd_client.repeat(0)
                self.mpd_client.single(0)
    
    def _media_shuffle(self):
        status = self.mpd_client.status()
        shuffle = status["random"]
        match shuffle:
            case "0":
                self.mpd_client.random(1)
            case "1":
                self.mpd_client.random(0)