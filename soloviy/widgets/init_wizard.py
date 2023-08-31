import attrs
import asyncio
from enum import Enum
from PySide6.QtCore import QObject, Signal, QDir, QPropertyAnimation, QSize
from PySide6.QtWidgets import QWizard, QMainWindow
from soloviy.ui.ui_init_wizard import Ui_Wizard
from soloviy.config import settings
from soloviy.api.mpd_connector import ConnectionStatus


class AlertStyle(Enum):
    NO_STYLE = ""
    ERROR = "background-color: #e95151;"
    WARNING = "background-color: #f09952;"
    SUCCESS = "background-color: #93cf4c;"
    

class AlertSize(Enum):
    OPEN = QSize(100500, 50)
    CLOSED = QSize(100500, 0)
    

class SignalsMixin:
    # Connect to mpd with chosen socket
    connect_mpd: Signal = Signal(str)


@attrs.define
class InitWizard(QWizard, Ui_Wizard, SignalsMixin):
    parent: QMainWindow
    socket: str = None
    alert_anim: QPropertyAnimation = attrs.field()
    
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.__attrs_init__(parent)
    
    def __attrs_pre_init__(self):
        QDir.addSearchPath("icons", "./soloviy/ui/icons/") 
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        self.mpd_socket_type.currentIndexChanged.connect(self.__socket_type_combo_box)

    @alert_anim.default
    def _alert_anim_init(self):
        anim = QPropertyAnimation(self.alert, b"maximumSize")
        return anim
    
    def __socket_type_combo_box(self):
        match self.mpd_socket_type.currentText():
            case "Built-in":
                self.mpd_socket.setEnabled(False)
            case "External":
                self.mpd_socket.setEnabled(True)

    def __connect_mpd(self):
        match self.mpd_socket_type.currentText():
            case "Built-in":
                self.socket = settings.mpd.native_socket
            case "External":
                self.socket = self.mpd_socket.text()
        self.connect_mpd.emit(self.socket)
    
    async def alert_trigger(self, style: AlertStyle = AlertStyle.NO_STYLE, 
                            text: str = "", timeout: float = 2):
        if self.alert_anim.endValue != AlertSize.CLOSED.value:
            self.alert_anim.setEndValue(AlertSize.CLOSED.value)
            self.alert_anim.setDuration(0)
            self.alert_anim.start()
        self.alert.setStyleSheet(style.value)
        self.alert_text.setText(text)
        self.alert_anim.setDuration(250)
        self.alert_anim.setEndValue(AlertSize.OPEN.value)
        self.alert_anim.start()
        await asyncio.sleep(timeout)
        self.alert_anim.setEndValue(AlertSize.CLOSED.value)
        self.alert_anim.start()        

    async def connect_mpd_tracker(self, status):
        match status:
            case ConnectionStatus.CONNECTING:
                await self.alert_trigger(AlertStyle.WARNING, "Connecting to mpd ...")
            case ConnectionStatus.CONNECTED:
                await self.alert_trigger(AlertStyle.SUCCESS, "Connection successful", 
                                         timeout = 1)
                settings.set("mpd.socket", self.socket)
                self.setCurrentId(self.nextId())
            case ConnectionStatus.CONNECTION_FAILED:
                await self.alert_trigger(AlertStyle.ERROR, "Failed to connect")
    
    def validateCurrentPage(self) -> bool:
        if self.currentPage() == self.wizardMPDConfig and not settings.mpd.socket:
            # IF current page is mpd config and connection is not established
            self.__connect_mpd()
            return False
        return True