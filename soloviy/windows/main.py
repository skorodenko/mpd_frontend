import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from pyqtconfig import ConfigManager
from ..utils.mpd_connector import MpdConnector
from ..widgets.ui_main import Ui_MainWindow
from ..constants import APP_CONFIG_FILE, APP_DEFAULT_SETTINGS


class MainWindow(QMainWindow, Ui_MainWindow, MpdConnector):
    
    def __playback_control_init(self):
        self.media_previous.setIcon(QIcon.fromTheme("media-skip-backward"))
        self.media_play_pause.setIcon(QIcon.fromTheme("media-playback-start"))
        self.media_next.setIcon(QIcon.fromTheme("media-skip-forward"))

        self.media_previous.clicked.connect(self._media_previous)
        self.media_play_pause.clicked.connect(self._media_play_pause)
        self.media_next.clicked.connect(self._media_next)

    def __playlist_control_init(self):
        match self.config.get("media_repeat"):
            case "no":
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-none"))
            case "all":
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-all"))
            case "single":
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-single"))
        
        match self.config.get("media_shuffle"):
            case "no":
                self.media_shuffle.setIcon(QIcon.fromTheme("media-playlist-normal"))
            case "yes":
                self.media_shuffle.setIcon(QIcon.fromTheme("media-playlist-shuffle"))

    def __init_gui(self):
        self.__playback_control_init()
        self.__playlist_control_init()
    
    def __init__(self):
        super().__init__()

        self.config = ConfigManager(APP_DEFAULT_SETTINGS, filename=APP_CONFIG_FILE)

        self.setupUi(self)
        self.__init_gui()       
        
        self.show()
        
        if self.config.get("mpd_socket") is None:
            ... #TODO Add initial mpd config dialog
        else:
            self._mpd_connect(self.config.get("mpd_socket"))

    def _media_play_pause(self):
        match self.mpd_client.status()["state"]:
            case "pause" | "stop":
                self.media_play_pause.setIcon(QIcon.fromTheme("media-playback-start"))
                #TODO Add mpd client play
            case "play":
                self.media_play_pause.setIcon(QIcon.fromTheme("media-playback-pause"))
                #TODO Add mpd client pause
    
    def _media_previous(self):
        ... #TODO Add mpd client previous
    
    def _media_next(self):
        ... #TODO Add mpd client next

    def closeEvent(self, event):
        self._mpd_disconnect()
        super().closeEvent(event)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())