import attrs
import asyncio
import qtinter
import logging
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHeaderView
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models.qmodels import PlaylistModel


logger = logging.getLogger(__name__)


class SignalsMixin:
    lock: Signal = Signal(object, bool)
    destroy: Signal = Signal(object)


@attrs.define
class PlaylistTile(QFrame, Ui_Frame, SignalsMixin):
    playlist: str
    
    def __attrs_pre_init__(self):
        super().__init__()
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        pmodel = PlaylistModel(self.playlist)
        self.playlist_table.setModel(pmodel)
        self._bind_signals()
        logger.info(f"Added tile {self.playlist}")
    
    def _bind_signals(self):
        self.playlist_lock.toggled.connect(
            lambda status: self.lock.emit(self, status)
        )
        self.playlist_destroy.clicked.connect(
            lambda: self.destroy.emit(self)
        )
