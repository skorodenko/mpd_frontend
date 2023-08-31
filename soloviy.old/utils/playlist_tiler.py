from attr import define, field, Factory
from typing import Deque
from collections import deque
from PyQt6 import QtWidgets, sip


@define
class PlaylistTiler:
    widget: QtWidgets.QMainWindow
    order: Deque = Factory(deque)
    lock: Deque = Factory(deque)
    mode: int = None
    
    @property
    def free(self):
        return len(self.order)
    
    @property
    def locked(self):
        return len(self.lock)

    @property    
    def free_space(self):
        return self.locked < self.mode

    def set_tile_mode(self, mode):
        if mode in ["1","2","3","4"]:
            self.mode = int(mode)
        else:
            raise ValueError(f"Bad tiling mode: {mode}")

    async def add_tile(self, tile):
        if self.locked + self.free == self.mode:
            old_tile = self.order.pop()
            await self.widget.playlist_destroy(old_tile, update=False, popped=True)
        self.order.appendleft(tile)
        await self.__update_tiling()
    
    async def destroy_tile(self, tile, update, popped):
        if tile in self.lock:
            del self.lock[self.lock.index(tile)]
        elif not popped:
            del self.order[self.order.index(tile)]
        if update:
            await self.__update_tiling()

    async def lock_tile(self, tile):
        del self.order[self.order.index(tile)]
        self.lock.append(tile)
        await self.__update_tiling()
    
    async def unlock_tile(self, tile):
        del self.lock[self.lock.index(tile)]
        self.order.appendleft(tile)
        await self.__update_tiling()

    async def __update_tiling(self):
        layout = QtWidgets.QGridLayout()
        for w,p in zip(self.lock + self.order,self.__get_tiling(self.free + self.locked)):
            layout.addWidget(w, *p)
        if (old_layout := self.widget.layout()) is not None:
            self.__delete_layout(old_layout)
        self.widget.setLayout(layout)
        self.__even_stretch(layout)

    def __delete_layout(self, cur_lay):
        if cur_lay is not None:
            while cur_lay.count():
                item = cur_lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(cur_lay)
    
    def __get_tiling(self, count):
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
                return ()
    
    def __even_stretch(self,layout):
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)