import time
from mpd import MPDClient
from PyQt6.QtCore import QProcess
from ..constants import MPD_NATIVE_SOCKET, MPD_NATIVE_CONFIG_FILE


class MpdConnector():
    def _mpd_connect(self, socket=MPD_NATIVE_SOCKET):
        if socket == MPD_NATIVE_SOCKET:
            self.mpd_server = QProcess()
            self.mpd_server.start("mpd", [MPD_NATIVE_CONFIG_FILE, "--no-daemon"])
        
        if self.mpd_server.waitForStarted():
            time.sleep(0.5)
            self.mpd_client = MPDClient()
            self.mpd_client.connect(socket)
    
    def _mpd_disconnect(self):
        self.mpd_client.close()
        self.mpd_server.terminate()
        self.mpd_server.waitForFinished(-1)