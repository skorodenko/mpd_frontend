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
    

@attrs.define
class TilingAPI:
    tiles: List[MetaTile] = attrs.field(init=False)
    sender: SignalSender = attrs.Factory(SignalSender)
    
    @tiles.default
    def _preload_tiles(self):
        if not state.get("tiles", False):
            state["tiles"] = list()
        return state["tiles"]
        
    def persist_changes(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            res = fun(self, *args, **kwargs)
            state["tiles"] = self.tiles
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
    
    def change_song(self, field: str, status: dict):
        ...
    
    @persist_changes  
    def clear(self):
        self.tiles.clear()