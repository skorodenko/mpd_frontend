import attrs
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from soloviy.frontend.ui.ui_playlist_tile import Ui_Frame
from soloviy.frontend import qmodels
# from soloviy.api.tiling import QMetaTile
# from soloviy.api.mpd_connector import MPDAction


class SignalsMixin:
    ...
    # Emit signal when toggling lock
    # lock: Signal = Signal(QMetaTile)
    # Emit signal when destroying tile
    # destroy: Signal = Signal(QMetaTile)
    # Emit on change of meta
    # metatile_updated: Signal = Signal(QMetaTile, MPDAction)


@attrs.define
class PlaylistTile(QFrame, Ui_Frame, SignalsMixin):
    # qmeta: QMetaTile

    def __attrs_pre_init__(self):
        super().__init__()

    def __attrs_post_init__(self):
        self.setupUi(self)
        self.playlist_lock.setChecked(self.qmeta.locked)
        self.playlist_title.setText(self.qmeta.name)
        pmodel = qmodels.PlaylistModel(self.qmeta)
        self.playlist_table.horizontalHeader().setSortIndicator(
            pmodel.columns.index(self.qmeta.order_by[0]),
            self.qmeta.order_by[1],
        )
        self.playlist_table.setModel(pmodel)
        self._bind_signals()

    def _bind_signals(self):
        self.playlist_lock.toggled.connect(lambda: self.lock.emit(self.qmeta))
        self.playlist_destroy.clicked.connect(lambda: self.destroy.emit(self.qmeta))
        # self.playlist_table.horizontalHeader().sectionClicked.connect(
        #    lambda _: self.qmetatile_updated.emit(self.qmeta, MPDAction.SORT)
        # )
        self.playlist_table.doubleClicked.connect(self._song_changed)

    def _song_changed(self, index):
        pos = index.row()
        self.qmeta.playing_pos = pos
        # self.qmetatile_updated.emit(self.qmeta, MPDAction.SONG_CHANGE)
