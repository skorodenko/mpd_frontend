import attrs
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHeaderView
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models import dbmodels, qmodels


class SignalsMixin:
    lock: Signal = Signal(object, bool)
    destroy: Signal = Signal(object)


@attrs.define
class PlaylistTile(QFrame, Ui_Frame, SignalsMixin):
    playlist: str
    
    def __attrs_pre_init__(self):
        super().__init__()
        self.setupUi(self)
        self._bind_signals()
    
    def __attrs_post_init__(self):
        dbmodels.PlaylistTile.create(name = self.playlist)
    
    def populated(self):
        pmodel = qmodels.PlaylistModel(self.playlist)
        self.playlist_table.setModel(pmodel)

    def delete(self):
        self.deleteLater()
        m = dbmodels.PlaylistTile
        m.delete().where(m.name == self.playlist).execute()
    
    def _bind_signals(self):
        self.playlist_lock.toggled.connect(
            lambda status: self.lock.emit(self, status)
        )
        self.playlist_destroy.clicked.connect(
            lambda: self.destroy.emit(self)
        )
