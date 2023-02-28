import asyncio
from collections import deque
from PyQt5 import QtWidgets, sip


class PlaylistTiler:
    def __init__(self, widget):
        self.widget = widget
        self.order = deque()
        self.lock = set()

    @property
    def free(self):
        return len([i for i in self.order if i not in self.lock])
    
    @property
    def locked(self):
        return len([i for i in self.order if i in self.lock])

    @property    
    def free_space(self):
        return self.locked < self.mode

    def set_tile_mode(self, mode):
        if mode in ["1","2","3","4"]:
            self.mode = int(mode)
        else:
            raise ValueError(f"Bad tiling mode: {mode}")

    def add_tile(self, tile):
        print(self.locked, self.free, self.mode)
        if self.locked + self.free == self.mode:
            old_tile = self.pop_free_tile()
            asyncio.create_task(self.widget.playlist_destroy(old_tile, update=False))
        self.order.append(tile)
        self.__update_tiling()
    
    def destroy_tile(self, tile, update):
        if tile in self.lock:
            self.lock.remove(tile)
        del self.order[self.order.index(tile)]
        if update:
            self.__update_tiling()

    def pop_free_tile(self):
        for t in self.order:
            if t not in self.lock:
                return t
    
    def lock_tile(self, tile):
        self.lock.add(tile)
    
    def unlock_tile(self, tile):
        self.lock.remove(tile)    

    def __update_tiling(self):
        layout = QtWidgets.QGridLayout()
        for w,p in zip(self.order, self.__get_tiling(self.free + self.locked)):
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