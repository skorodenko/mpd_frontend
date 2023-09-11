import attrs
import logging
from weakref import WeakValueDictionary
from peewee import fn
from typing import Optional
from soloviy.models import dbmodels
from soloviy.config import settings
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout
from soloviy.widgets.playlist_tile import PlaylistTile


logger = logging.getLogger(__name__)


class SignalsMixin:
    # Emmited when playlist metadata inserted into db
    playlist_created: Signal = Signal(str)
    tile_layout_update: Signal = Signal()


@attrs.define
class PTilingWidget(QWidget, SignalsMixin):
    tiles: WeakValueDictionary = WeakValueDictionary()
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__attrs_init__()
    
    def __attrs_post_init__(self):
        self.tile_layout_update.connect(
            self.tiles_update
        )
        layout = QGridLayout(self)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)
        self.setLayout(layout)
        logger.info("Created widget")
    
    def _bind_tile_signals(self, tile: PlaylistTile):
        tile.lock.connect(
            self.__manage_tile_lock
        )
        tile.destroy.connect(
            self.__manage_tile_destruction
        )
    
    @property
    def free(self) -> int:
        m = dbmodels.PlaylistTile
        return m.select().where(m.locked == False).count()
    
    @property
    def locked(self) -> int:
        m = dbmodels.PlaylistTile
        return m.select().where(m.locked == True).count()

    @property    
    def free_space(self) -> bool:
        return self.locked < settings.soloviy.tiling_mode
    
    @property
    def overflow_space(self) -> bool:
        return self.locked + self.free == settings.soloviy.tiling_mode
    
    def tile_placed(self, playlist: str) -> Optional[PlaylistTile]:
        m = dbmodels.PlaylistTile
        return m.select().where(m.name == playlist).first()
        
    def tile_add(self, playlist: str):
        logger.debug(f"Adding tile {playlist}")
        if self.tile_placed(playlist):
            logger.debug(f"Tile already added {playlist}")
            return
        elif self.free_space:
            if self.overflow_space:
                inst = dbmodels.PlaylistTile \
                    .select() \
                    .where(dbmodels.PlaylistTile.locked == False) \
                    .order_by(dbmodels.PlaylistTile.tile_order, 
                              dbmodels.PlaylistTile.locked) \
                    .first()
                logger.debug(f"Removing last tile {inst.name}")
                self.tile_destroy(inst.name)
            self.tiles[playlist] = PlaylistTile(playlist)
            self.playlist_created.emit(playlist)
            logger.debug(f"Added tile {playlist}")
    
    def tile_destroy(self, playlist: str):
        layout = self.layout()
        tile = self.tiles[playlist]
        layout.removeWidget(tile)
        tile.delete()
        del tile
        logger.debug(f"Destroyed tile {playlist}")
    
    def tiles_update(self):
        logger.debug("Updating tiles")
        layout = self.layout()
        m = dbmodels.PlaylistTile
        query = m.select().order_by(m.tile_order.desc(), m.locked)
        for plst, pos in zip(query,self.__get_tiling(self.free + self.locked)):
            tile = self.tiles.get(plst.name)
            tile.populated()
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
    
    def __manage_tile_lock(self, tile: PlaylistTile, locked: bool):
        if locked:
            del self.order[self.order.index(tile)]
            self.lock.append(tile)
        else:
            del self.lock[self.lock.index(tile)]
            self.order.appendleft(tile)
        self.tile_layout_update.emit()
    
    def __manage_tile_destruction(self, tile: PlaylistTile):
        self.tile_destroy(tile)
        self.tile_layout_update.emit()