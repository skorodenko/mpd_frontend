import attrs
import logging
import qtinter
import pathlib
import datetime
from soloviy.db import state
from soloviy.config import settings
from soloviy.models import dbmodels as db
from soloviy.models.qtmodels import PlaylistsModel
from soloviy.api.mpd_connector import MpdConnector
from soloviy.ui.ui_main_window import Ui_MainWindow
from soloviy.widgets.init_wizard import InitWizard
from soloviy.widgets.settings import Settings
from PySide6.QtGui import QActionGroup, QAction, QIcon, QPixmap, QFont
from PySide6.QtCore import QDir, QTimer, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QDialog, QApplication


logger = logging.getLogger(__name__)


class SignalsMixin:
    # Emitted when db update is needed
    update_db: Signal = Signal()
    # Emitted when group_by changed
    update_ui: Signal = Signal()


@attrs.define
class MainWindow(QMainWindow, Ui_MainWindow, SignalsMixin):
    timer: QTimer = QTimer
    mpd: MpdConnector = attrs.Factory(MpdConnector)
    init_wizard: InitWizard = attrs.Factory(InitWizard, takes_self=True)
    settings: Settings = attrs.Factory(Settings, takes_self=True)
    
    def __attrs_pre_init__(self):
        super().__init__()
        QDir.addSearchPath("icons", "./soloviy/ui/icons/") 
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        self._bind_signals()
        self._init_state()
        self._ui_post_init()
        self._bind_buttons()
        
    def serve(self):
        logger.info("Started main window")
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, self._initial_configuration)
 
    def _initial_configuration(self):
        logger.info("Started initial configuration")
        if not settings.mpd.socket:
            if self.init_wizard.exec() == QDialog.DialogCode.Rejected:
                self.close()
            else:
                self.update_db.emit()
                #self.settings.persist_settings()
        else:
            self.init_wizard.connect_mpd.emit(settings.mpd.socket)
    
    def _init_state(self):
        logger.debug("Initializing state variables")
        if not state.get("group_by", None):
            state["group_by"] = settings.default.group_by
        if state.get("prev_tile"):
            state["prev_tile"] = None
            
    def _ui_post_init(self):
        # Init menubar actions [Group by]
        group = state["group_by"]
        self.group_by_actions = QActionGroup(self)
        self.group_by_actions.setExclusive(True)
        self.group_by_actions.triggered.connect(self.__group_by_changed)
        actions = [self.actionDirectory, self.actionAlbum, self.actionAlbumartist,
                   self.actionArtist, self.actionComposer, self.actionDate,
                   self.actionFormat, self.actionGenre]
        for a in actions:
            if group == a.text().lower():
                a.setChecked(True)
            self.group_by_actions.addAction(a)
        
        # Font setup
        light_font = QApplication.font()
        light_font.setWeight(QFont.Weight.Light)
        self.label_time.setFont(light_font)
        self.label_author.setFont(light_font)
        self.label_info.setFont(light_font)
    
    def _bind_buttons(self):
        self.media_play_pause.clicked.connect(
            qtinter.asyncslot(self.mpd.media_play_pause)
        )
        self.media_next.clicked.connect(
            qtinter.asyncslot(self.mpd.media_next)
        )
        self.media_previous.clicked.connect(
            qtinter.asyncslot(self.mpd.media_previous)
        )
        self.media_repeat.clicked.connect(
            qtinter.asyncslot(self.mpd.media_repeat)
        )
        self.media_shuffle.clicked.connect(
            qtinter.asyncslot(self.mpd.media_shuffle)
        )
        self.media_seek.sliderMoved.connect(
            qtinter.asyncslot(self.mpd.media_seeker)
        )
    
    def _bind_signals(self):
        self.mpd.mpd_connection_status.connect(
            self.init_wizard.connect_mpd_tracker
        )
        self.update_db.connect(
            qtinter.asyncslot(self.mpd.update_db)
        )
        self.ptiling_widget.tile_mpd_gate.connect(
            qtinter.asyncslot(self.mpd._handle_tile_gateway)
        )
        self.mpd.db_updated.connect(
            lambda: self.update_ui.emit()
        )
        self.update_ui.connect(
            self.__update_playlists_view
        )
        self.update_ui.connect(
            lambda: self.ptiling_widget.tile_layout_update.emit()
        )
        self.init_wizard.connect_mpd.connect(
            qtinter.asyncslot(self.mpd.mpd_connect)
        )
        self.playlists_view.doubleClicked.connect(
            lambda pname: self.ptiling_widget.add_tile(pname.data())
        )
        self.mpd.mpd_idle_update.connect(
            self.__mpd_idle_update
        )
        self.mpd.song_changed.connect(
            self.__song_changed
        )
        self.mpd.update_seeker.connect(
            self.__update_seeker
        )
        self.mpd.mpd_idle_update.connect(
            self.ptiling_widget._mpd_idle_update
        )
        
    @Slot(str, dict)
    def __mpd_idle_update(self, field: str, status: dict):
        match field:
            case "state":
                match status["state"]:
                    case "play":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-pause")
                        )
                    case "pause":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-start")
                        )
                    case "stop":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-start")
                        )
            
            case "repeat" | "single":
                match status["repeat"], status["single"]:
                    case ("0","0") | ("0","1"): #Second variant is redundant
                        self.media_repeat.setIcon(
                            QIcon.fromTheme("media-repeat-none")
                        )
                    case ("1","0"):
                        self.media_repeat.setIcon(
                            QIcon.fromTheme("media-repeat-all")
                        )
                    case ("1","1"):
                        self.media_repeat.setIcon(
                            QIcon.fromTheme("media-repeat-single")
                        )
            
            case "random":
                if status["random"] == "0":
                    self.media_shuffle.setIcon(
                        QIcon.fromTheme("media-playlist-normal")
                    )
                else:
                    self.media_shuffle.setIcon(
                        QIcon.fromTheme("media-playlist-shuffle")
                    )
    
    @staticmethod
    def strfdelta(tdelta):
        h, rem = divmod(tdelta.seconds, 3600)
        m, s = divmod(rem, 60)
        match h,m,s:
            case h,_,_ if h != 0:
                return f"{h}:{m:0>2}:{s:0>2}"
            case _:
                return f"{m:0>2}:{s:0>2}"
    
    @Slot(int, int)
    def __update_seeker(self, duration: int, elapsed: int):
        dd = datetime.timedelta(seconds=duration)
        ed = datetime.timedelta(seconds=elapsed)
        
        self.label_time.setText(f"{self.strfdelta(ed)}/{self.strfdelta(dd)}")
        if self.media_seek.maximum() != duration:
            self.media_seek.setMaximum(duration)
        self.media_seek.setSliderPosition(elapsed)
                 
    @Slot(dict, QPixmap)
    def __song_changed(self, info: dict, cover: QPixmap):
        title = info.get("title", "Title")
        artist = info.get("artist", "Artist")
        album = info.get("album", "Album")
        form = info.get("format", "0:0:0")
        freq, bitr, _ = form.split(":")
        file = info.get("file", "blank.ext")
        _, ext = pathlib.Path(file).suffix.upper().split(".")
        self.label_title.setText(title)
        self.label_author.setText(f"{artist} | {album}")
        self.label_info.setText(f"{int(freq)/1000} kHz, {bitr} bit, {ext}")
        self.label_art.setPixmap(cover)
    
    @Slot(QAction)
    def __group_by_changed(self, action: QAction):
        group = action.text().lower()
        state["group_by"] = group
        self.update_ui.emit()
    
    @Slot()
    def __update_playlists_view(self):
        logger.debug("Updating playlists view")
        group = state.get("group_by", settings.default.group_by)
        sql_group = getattr(db.Library, group)
        query = (db.Library
                    .select(sql_group)
                    .order_by(sql_group)
                    .distinct())
        playlists = [getattr(i, group) for i in query]
        playlists_model = PlaylistsModel(playlists)
        self.playlists_view.setModel(playlists_model)
    
    def closeEvent(self, event):
        logger.info("Closing main window")
        self.mpd.graceful_close()
        super().closeEvent(event)
    