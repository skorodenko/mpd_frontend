import time
import sys
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
                break
            except (ConnectionRefusedError, AttributeError, ValueError):
                if not MpdSocketConfig(self).exec():
                    sys.exit()
