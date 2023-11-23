import attrs
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models import qtmodels
from soloviy.api.tiling import MetaTile
from soloviy.api.mpd_connector import MPDAction


class SignalsMixin:
    # Emit signal when toggling lock
    lock: Signal = Signal(MetaTile)
    # Emit signal when destroying tile
    destroy: Signal = Signal(MetaTile)
    # Emit on change of meta
    metatile_updated: Signal = Signal(MetaTile, MPDAction)


@attrs.define
class PlaylistTile(QFrame, Ui_Frame, SignalsMixin):
    meta: MetaTile
    
    def __attrs_pre_init__(self):
        super().__init__()
    
    def __attrs_post_init__(self):
        self.setupUi(self)
        self.playlist_lock.setChecked(self.meta.locked)
        self.playlist_title.setText(self.meta.name)
        pmodel = qtmodels.PlaylistModel(self.meta)
        #self.playlist_table.horizontalHeader().setSortIndicator
        self.playlist_table.setModel(pmodel)
        self._bind_signals()
    
    def _bind_signals(self):
        self.playlist_lock.toggled.connect(
            lambda: self.lock.emit(self.meta)
        )
        self.playlist_destroy.clicked.connect(
            lambda: self.destroy.emit(self.meta)
        )
        self.playlist_table.horizontalHeader().sectionClicked.connect(
            lambda _: self.metatile_updated.emit(self.meta, MPDAction.SORT)
        )
        self.playlist_table.doubleClicked.connect(
            self._song_changed
        )
        
    def _song_changed(self, index):
        pos = index.row()
        self.meta.playing_pos = pos
        self.metatile_updated.emit(self.meta, MPDAction.SONG_CHANGE)
