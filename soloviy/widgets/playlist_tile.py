import attrs
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHeaderView
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models import dbmodels, qtmodels
from soloviy.api.tiling import MetaTile


class SignalsMixin:
    # Emit signal when toggling lock
    lock: Signal = Signal(MetaTile)
    # Emit signal when destroying tile
    destroy: Signal = Signal(MetaTile)
    # Emit on change in metadata
    update_metadata: Signal = Signal()


@attrs.define
class PlaylistTile(QFrame, Ui_Frame, SignalsMixin):
    meta: MetaTile
    
    def __attrs_pre_init__(self):
        super().__init__()
    
    def __attrs_post_init__(self):
        self.setupUi(self)
        self.playlist_lock.setChecked(self.meta.locked)
        self.playlist_title.setText(self.meta.name)
        self._bind_signals()
        pmodel = qtmodels.PlaylistModel(self.meta)
        self.playlist_table.setModel(pmodel)
    
    def _bind_signals(self):
        self.playlist_lock.toggled.connect(
            lambda: self.lock.emit(self.meta)
        )
        self.playlist_destroy.clicked.connect(
            lambda: self.destroy.emit(self.meta)
        )
