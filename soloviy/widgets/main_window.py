import attrs
import logging
import qtinter
from PIL import Image, ImageQt
from io import BytesIO
from dynaconf.loaders.toml_loader import write
from PySide6.QtCore import QDir, QTimer, Signal, QObject, Slot
from PySide6.QtWidgets import QMainWindow, QDialog
from soloviy.config import settings
from soloviy.models import dbmodels as db
from soloviy.models.qmodels import PlaylistsModel
from soloviy.api.mpd_connector import MpdConnector
from soloviy.ui.ui_main_window import Ui_MainWindow
from soloviy.widgets.init_wizard import InitWizard


logger = logging.getLogger(__name__)


class SignalsMixin:
    update_db: Signal = Signal()


@attrs.define
class MainWindow(QMainWindow, Ui_MainWindow, SignalsMixin):
    timer: QTimer = QTimer
    mpd: MpdConnector = attrs.Factory(MpdConnector)
    init_wizard: InitWizard = attrs.Factory(InitWizard, takes_self=True)
    
    def __attrs_pre_init__(self):
        super().__init__()
        QDir.addSearchPath("icons", "./soloviy/ui/icons/") 
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        self._bind_signals()
        
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
                #self.persist_settings()
                ... # Updated db
        else:
            self.init_wizard.connect_mpd.emit(settings.mpd.socket)
    
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
        self.init_wizard.connect_mpd.connect(
            qtinter.asyncslot(self.mpd.mpd_connect)
        )
        self.playlists_view.doubleClicked.connect(
            lambda pname: self.ptiling_widget.tile_add(pname.data())
        )
    
    @Slot()
    def __update_playlists_view(self):
        #TODO Add various groupping options
        query = (db.Library
                    .select(db.Library.directory)
                    .order_by(db.Library.directory)
                    .distinct())
        playlists = [i.directory for i in query]
        playlists_model = PlaylistsModel(playlists)
        self.playlists_view.setModel(playlists_model)
    
    @staticmethod
    def persist_settings(): #TODO move to settings widget
        logger.info("Persisted settings")
        data = settings.as_dict()
        write(settings.settings_file, data)
        
    def closeEvent(self, event):
        logger.info("Closing main window")
        self.mpd.graceful_close()
        super().closeEvent(event)
    