import attrs
from functools import wraps
from typing import List, Optional, Tuple
from soloviy.db import state
from soloviy.config import settings
from PySide6.QtCore import Qt, QObject, Signal


class Exceptions:
    class TileDoesNotExist(Exception):
        ...
        
    class TileLocked(Exception):
        ...


class SignalSender(QObject):
    # Emit on setattr in metatile
    meta_updated: Signal = Signal()


@attrs.define
class MetaTile:
    name: str
    locked: bool = False
    order_by: Tuple[str, Qt.SortOrder] = ("track", Qt.SortOrder.AscendingOrder) # ADD SETTINGS ENTRY
    #group_by: Optional[str] = attrs.Factory(lambda: state["group_by"])
    playing_pos: Optional[int] = None
    
    
class QMetaTile(QObject):
    meta_changed: Signal = Signal(str)
    
    def __init__(self, tile: MetaTile):
        self._tile: MetaTile = tile
    
    @property
    def meta(self):
        return self._tile
    
    @property  
    def name(self):
        return self._tile.name
    
    @name.setter
    def _name_set(self, val: str):
        self._tile.name = val
        self.meta_changed.emit("name")
    
    @property
    def locked(self):
        return self._tile.locked
    
    @locked.setter
    def _locked_set(self, val: bool):
        self._tile.locked = val
        self.meta_changed.emit("locked")

    @property
    def order_by(self):
        return self._tile.order_by
    
    @order_by.setter
    def _order_by_set(self, val: Tuple[str, Qt.SortOrder]):
        self._tile.order_by = val
        self.meta_changed.emit("order_by")
    
    @property
    def playing_pos(self):
        return self._tile.playing_pos
    
    @playing_pos.setter
    def _playing_pos_set(self, val):
        self._tile.playing_pos = val
        self.meta_changed.emit("playing_pos")
    

@attrs.define
class TilingAPI:
    tiles: List[QMetaTile] = attrs.field(init=False)
    sender: SignalSender = attrs.Factory(SignalSender)
    
    @tiles.default
    def _preload_tiles(self):
        if not state.get("tiles", False):
            tiles = list()
            state["tiles"] = tiles
        else:
            meta_tiles = state["tiles"]
            tiles = [QMetaTile(t) for t in meta_tiles]
        return tiles
        
    def persist_changes(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            res = fun(self, *args, **kwargs)
            meta_tiles = list(map(lambda t: t.meta, self.tiles))
            state["tiles"] = meta_tiles
            return res
        return wrapper

    @property
    def tmode(self) -> int:
        return settings.soloviy.tiling_mode
    
    @property
    def locked(self) -> int:
        return sum(1 for tile in self.tiles if tile.locked)
    
    @property
    def first_unlocked(self) -> Optional[int]:
        for i, tile in enumerate(self.tiles):
            if not tile.locked:
                return i
    
    #Slot
    @persist_changes
    def update_metadata(self):
        ...
    
    #Slot
    @persist_changes
    def add_tile(self, tile: MetaTile):
        if self.locked + 1 > self.tmode:
            # raise Exceptions.TileLocked(f"All tiles locked: {self.tmode}")
            return
        if tile in self.tiles:
            return 
        tile = QMetaTile(tile)
        if len(self.tiles) + 1 > self.tmode: # Rotate free tiles
            index = self.first_unlocked
            self.tiles.pop()
            self.tiles.insert(index, tile)
        else: # Just append tile
            self.tiles.append(tile)
        self.sender.meta_updated.emit()
    
    #Slot
    @persist_changes
    def toggle_lock_tile(self, tile: MetaTile):
        if tile.locked:
            tile.locked = False
            self.tiles.sort(key=lambda x: x.locked, reverse=True)
        else:
            tile.locked = True
            self.tiles.sort(key=lambda x: not x.locked)
    
    #Slot
    @persist_changes
    def remove_tile(self, tile: MetaTile):
        if tile not in self.tiles:
            raise Exceptions.TileDoesNotExist(f"{tile.name}")
        self.tiles.remove(tile)
    
    #Slot
    @persist_changes
    def change_playing_tile(self, tile: MetaTile):
        for _tile in self.tiles:
            if _tile is not tile:
                _tile.playing_pos = None
    
    @persist_changes
    def change_song(self, pos: Optional[int]):
        for tile in self.tiles:
            if tile.playing_pos is not None:
                if pos is None:
                    tile.playing_pos = pos
                else:
                    tile.playing_pos = int(pos)
        self.sender.meta_updated.emit()
    
    @persist_changes  
    def clear(self):
        self.tiles.clear()