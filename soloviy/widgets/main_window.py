import attrs
import logging
import qtinter
from PySide6.QtGui import QActionGroup, QAction
from PySide6.QtCore import QDir, QTimer, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QDialog
from soloviy.db import state
from soloviy.config import settings
from soloviy.models import dbmodels as db
from soloviy.models.qmodels import PlaylistsModel
from soloviy.api.mpd_connector import MpdConnector
from soloviy.ui.ui_main_window import Ui_MainWindow
from soloviy.widgets.init_wizard import InitWizard
from soloviy.widgets.settings import Settings


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
        self._ui_post_init()
        
    def serve(self):
        logger.info("Started main window")
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, self._initial_configuration)
 
    def _initial_configuration(self):
        logger.info("Started initial configuration")
        if not settings.mpd.socket:
            self.mpd.mpd_connection_status.connect(
                self.init_wizard.connect_mpd_tracker
            )
            if self.init_wizard.exec() == QDialog.DialogCode.Rejected:
                self.close()
            else:
                self.update_db.emit()
                #self.settings.persist_settings()
        else:
            self.init_wizard.connect_mpd.emit(settings.mpd.socket)
    
    def _ui_post_init(self):
        # Init menubar actions [Group by]
        group = state.get("group_by", settings.default.group_by)
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
    
    def _bind_signals(self):
        #self.playlists_view.doubleClicked.connect(
        #    qtinter.asyncslot(self.mpd.playlist_add_db)   
        #)
        self.update_db.connect(
            qtinter.asyncslot(self.mpd.update_db)
        )
        self.mpd.playlist_populated.connect(
            lambda: self.ptiling_widget.tile_layout_update.emit()  
        )
        self.mpd.db_updated.connect(
            self.__update_playlists_view
        )
        self.update_ui.connect(
            self.__update_playlists_view
        )
        self.init_wizard.connect_mpd.connect(
            qtinter.asyncslot(self.mpd.mpd_connect)
        )
        self.playlists_view.doubleClicked.connect(
            lambda pname: self.ptiling_widget.tile_add(pname.data())
        )
    
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
    