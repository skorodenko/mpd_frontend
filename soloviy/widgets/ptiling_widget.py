import attrs
import logging
from typing import Optional
from soloviy.models import dbmodels
from soloviy.config import settings
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout
from soloviy.widgets.playlist_tile import PlaylistTile
from soloviy.api.tiling import TilingAPI, MetaTile


logger = logging.getLogger(__name__)


class SignalsMixin:
    # Emitted when tile layout should be updated
    tile_layout_update: Signal = Signal()


@attrs.define
class PTilingWidget(QWidget, SignalsMixin):
    tiling_api: TilingAPI = attrs.Factory(TilingAPI)
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__attrs_init__()
    
    def __attrs_post_init__(self):
        self._bind_sgnals()
        layout = QGridLayout(self)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)
        self.setLayout(layout)
        logger.debug("Created tiling widget")
        
    def _bind_sgnals(self):
        self.tile_layout_update.connect(
            self.tiles_update
        )
    
    def _bind_tile_signals(self, tile: PlaylistTile):
        tile.lock.connect(
            self.tiling_api.toggle_lock_tile
        )
        tile.lock.connect(
            lambda: self.tile_layout_update.emit()
        )
        tile.destroy.connect(
            self.tiling_api.remove_tile
        )
        tile.destroy.connect(
            lambda: self.tile_layout_update.emit()
        )
    
    def _clear_layout(self):
        if layout := self.layout():
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)
    
    def add_tile(self, playlist: str):
        logger.debug(f"Adding tile: {playlist}")
        meta = MetaTile(playlist)
        self.tiling_api.add_tile(meta)
        self.tile_layout_update.emit()
    
    def tiles_update(self):
        logger.debug("Updating tiles")
        self._clear_layout()
        layout = self.layout()
        metadata = self.tiling_api.tiles
        #TODO Get rid of playlists which do not fit into new mode !note zip_longest
        for meta, pos in zip(metadata, self.__get_tiling(len(metadata))):
            tile = PlaylistTile(meta)
            self._bind_tile_signals(tile)
            layout.addWidget(tile, *pos)
        logger.debug("Updated tiles")

    def __get_tiling(self, count) -> list[tuple]:
        match count:
            case 1:
                return [(0,0,2,2)]
            case 2:
                return [(0,0,2,1),(0,1,2,1)]
            case 3:
                return [(0,0,2,1),(0,1,1,1),(1,1,1,1)]
            case 4:
                return [(0,0,1,1),(0,1,1,1),(1,0,1,1),(1,1,1,1)]
            case _:
                return []