import sys
import qtinter
from aiocache import Cache
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
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
        self.cache = Cache()
        
        super().__init__()

        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, qtinter.asyncslot(self._mpd_connect_dialog))

    async def _mpd_idle(self):
        self._idle_cache = await self.mpd_client.status()
        await self._init_gui(self._idle_cache)
        async for _ in self.mpd_client.idle():
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
                case "song" | "playlist":
                    await self._label_song_change()

    def closeEvent(self, event):
        self._mpd_disconnect(self.config.get("mpd_socket"))
        super().closeEvent(event)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with qtinter.using_asyncio_from_qt():
        main_window = MainWindow()
        sys.exit(app.exec())