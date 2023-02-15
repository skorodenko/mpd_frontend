import sys
import qtinter
from mpd.asyncio import MPDClient
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication
from pyqtconfig import ConfigManager
from ..widgets.init_main import InitMainWindow
from ..utils.mpd_connector import MpdConnector
from ..constants import APP_CONFIG_FILE, APP_DEFAULT_SETTINGS


class MainWindow(InitMainWindow, MpdConnector):
    
    @staticmethod
    def status_diff(old, new):
        return [k for k in old.keys() 
            if old.get(k) != new.get(k)
            and old.get(k) is not None
            and new.get(k) is not None]

    def __init__(self):
        QtCore.QDir.addSearchPath("logo", "./soloviy/resources/logo/")        
        self.config = ConfigManager(APP_DEFAULT_SETTINGS, filename=APP_CONFIG_FILE)
        self.timer = QtCore.QTimer 
        
        super().__init__()

        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, self._mpd_connect_dialog)

    async def _mpd_idle(self, socket):
        self.mpd_client = MPDClient()
        await self.mpd_client.connect(socket)
        self._idle_cache = await self.mpd_client.status()
        song = await self.mpd_client.currentsong()
        await self._init_gui(self._idle_cache, song)
        async for subsystem in self.mpd_client.idle():
            match subsystem:
                case ["player"] | ["options"]:
                    new = await self.mpd_client.status()
                    await self._route_async_changes(
                        self.status_diff(self._idle_cache, new),
                        new
                    )
                    self._idle_cache = new

    async def _route_async_changes(self, diff, status):
        for d in diff:
            match d:
                case "state":
                    state = status["state"]
                    await self._icon_media_play_pause(state)
                case "repeat" | "single":
                    repeat = status["repeat"]
                    single = status["single"]
                    await self._icon_media_repeat(repeat, single)
                case "random":
                    shuffle = status["random"]
                    await self._icon_media_shuffle(shuffle)
                case "song":
                    song = await self.mpd_client.currentsong()
                    await self._label_song_change(song)

    def closeEvent(self, event):
        self._mpd_disconnect(self.config.get("mpd_socket"))
        super().closeEvent(event)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with qtinter.using_asyncio_from_qt():
        main_window = MainWindow()
        sys.exit(app.exec())