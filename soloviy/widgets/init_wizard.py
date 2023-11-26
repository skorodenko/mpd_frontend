import attrs
import asyncio
import qtinter
from enum import Enum
from PySide6.QtCore import Signal, QDir, QPropertyAnimation, Slot
from PySide6.QtWidgets import QWizard, QMainWindow, QWidget, QLabel, QFileDialog
from soloviy.ui.ui_init_wizard import Ui_Wizard
from soloviy.db import state
from soloviy.config import settings
from soloviy.api.mpd_connector import ConnectionStatus


class AlertStyle(Enum):
    NO_STYLE = ""
    ERROR = "background-color: #e95151;"
    WARNING = "background-color: #f09952;"
    SUCCESS = "background-color: #93cf4c;"
    

class AlertSize(Enum):
    OPEN = 50
    CLOSED = 0
    
    
class AlertPage(Enum):
    wizardStart = 1
    wizardServerConfig = 2
    wizardLocalConfig = 3
    wizardFinish = 4
    

class SignalsMixin:
    # Connect to mpd with chosen socket
    connect_mpd: Signal = Signal(str)
    # Create db for current music library
    update_db: Signal = Signal()
    # Trigger alert
    alert: Signal = Signal(AlertPage, AlertStyle, str)


@attrs.define
class InitWizard(QWizard, Ui_Wizard, SignalsMixin):
    parent: QMainWindow
    socket: str = None
    mpd_binary: bool = attrs.field(init = False)
    
    @mpd_binary.default
    def _factory_mpd_binary(self) -> bool:
        from shutil import which
        return which("mpd") is not None
    
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.__attrs_init__(parent)
    
    def __attrs_pre_init__(self):
        QDir.addSearchPath("icons", "./soloviy/ui/icons/") 
        self.setupUi(self)
        
    def __attrs_post_init__(self):
        self.alert.connect(
            qtinter.asyncslot(self.alert_manager)   
        )
        self.wizardLocalConfig_filedialog.clicked.connect(
            self.music_collection_select
        )
    
    @Slot(AlertPage, AlertStyle, str)
    async def alert_manager(self, page: AlertPage, style: AlertStyle, text: str):
        """Alert manager which routes alert to respective wizard pages

        :param page: Wizard page
        :type page: AlertPage
        :param style: Stylesheet for alert
        :type style: AlertStyle
        :param text: Alert text
        :type text: str
        """
        match page:
            case AlertPage.wizardStart:
                await self.alert_trigger(self.wizardStart_alert, 
                                         self.wizardStart_alert_text,
                                         style, text)
            case AlertPage.wizardServerConfig:
                await self.alert_trigger(self.wizardServerConfig_alert, 
                                         self.wizardServerConfig_alert_text,
                                         style, text)
            case AlertPage.wizardLocalConfig:
                await self.alert_trigger(self.wizardLocalConfig_alert, 
                                         self.wizardLocalConfig_alert_text,
                                         style, text)
    
    async def alert_trigger(self, alert: QWidget, alert_text: QLabel, 
                            style: AlertStyle = AlertStyle.NO_STYLE, 
                            text: str = "", timeout: float = 2):
        """Controls animation process

        :param alert: Alert widget 
        :type alert: QWidget
        :param alert_text: Alert widget label
        :type alert_text: QLabel
        :param style: Alert stylesheet enum, defaults to AlertStyle.NO_STYLE
        :type style: AlertStyle, optional
        :param text: Alert text, defaults to ""
        :type text: str, optional
        :param timeout: Time after alert closes, defaults to 2
        :type timeout: float, optional
        """
        self.anim = QPropertyAnimation(alert, b"maximumHeight")
        if alert.maximumHeight() != AlertSize.CLOSED.value:
            alert.setMaximumHeight(AlertSize.CLOSED.value)
        alert.setStyleSheet(style.value)
        alert_text.setText(text)
        self.anim.setDuration(250)
        self.anim.setEndValue(AlertSize.OPEN.value)
        self.anim.start()
        await asyncio.sleep(timeout)
        self.anim.setEndValue(AlertSize.CLOSED.value)
        self.anim.start()        

    @Slot(ConnectionStatus)
    def connect_mpd_tracker(self, status: ConnectionStatus):
        """Slot to track the status of mpd connection

        :param status: Connection status enum
        :type status: ConnectionStatus
        """
        if self.currentPage() == self.wizardLocalConfig:
            page = AlertPage.wizardLocalConfig
        elif self.currentPage() == self.wizardServerConfig:
            page = AlertPage.wizardServerConfig
        match status:
            case ConnectionStatus.CONNECTING:
                self.alert.emit(page, AlertStyle.WARNING, "Connecting to mpd ...")
            case ConnectionStatus.CONNECTED:
                self.alert.emit(page, AlertStyle.SUCCESS, "Connection successful")
                settings.set("mpd.socket", self.socket)
                self.setCurrentId(self.nextId())
            case ConnectionStatus.CONNECTION_FAILED:
                self.alert.emit(page, AlertStyle.ERROR, "Failed to connect")
    
    @Slot()
    def music_collection_select(self):
        """Slot to select music collection root folder"""
        self.file_dialog = QFileDialog(self)
        d = self.file_dialog.getExistingDirectory(self, 
                                                  "Select music collection root")   
        self.wizardLocalConfig_musicfolder_text.setText(d)
        state["music_folder"] = d
    
    def initializePage(self, id: int) -> None:
        if self.page(id) == self.wizardStart:
            self.radio_local.setEnabled(True)
            self.radio_local_text.setEnabled(True)
        return super().initializePage(id)
    
    def nextId(self) -> int:
        """Return id of next wizard page based on current page

        :return: id of next page
        :rtype: int
        """
        pages = [self.page(i) for i in self.pageIds()]
        match self.currentPage():
            case self.wizardStart:
                if self.radio_server.isChecked():
                    return pages.index(self.wizardServerConfig) + 1
                if self.radio_local.isChecked():
                    return pages.index(self.wizardLocalConfig) + 1
            case self.wizardLocalConfig | self.wizardServerConfig:
                return pages.index(self.wizardFinish) + 1       
        return super().nextId()
    
    def validateCurrentPage(self) -> bool:
        """Validate current page before going to next one

        :return: True if page valid, False otherwise
        :rtype: bool
        """
        cpage = self.currentPage()
        if cpage == self.wizardStart:
            rlocal = self.radio_local.isChecked()
            rserver = self.radio_server.isChecked()
            if not (rlocal or rserver):
                self.alert.emit(AlertPage.wizardStart, 
                                AlertStyle.ERROR, 
                                "Please select setup type")
                return False
        if cpage == self.wizardServerConfig and not settings.mpd.socket:
            host = self.wizardServerConfig_host.text()
            port = self.wizardServerConfig_port.text()
            password = self.wizardServerConfig_password.text()
            
            match host, port, password:
                case _, "0", "":
                    socket = host
                case _, _, "" if port != "0":
                    socket = f"{host}:{port}"
                
            self.socket = socket
            self.connect_mpd.emit(self.socket)
            return False
        if cpage == self.wizardLocalConfig and not settings.mpd.socket:
            if not self.wizardLocalConfig_musicfolder_text.text():
                self.alert.emit(AlertPage.wizardLocalConfig, 
                                AlertStyle.ERROR, 
                                "Please select music collection")
            else:
                socket = settings.mpd.native_socket
                self.socket = socket
                self.connect_mpd.emit(self.socket)
            return False
        return True