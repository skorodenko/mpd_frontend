import attrs
import asyncio
import itertools
from typing import Optional
from soloviy.config import settings
from collections import deque
from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QWidget, QGridLayout
#from soloviy.utils.playlist_tiler import PlaylistTiler
from soloviy.widgets.playlist_tile import PlaylistTile


class SignalsMixin:
    tile_mode_updated: Signal = Signal()
    tile_layout_update: Signal = Signal()

@attrs.define
class PTilingWidget(QWidget, SignalsMixin):
    order: deque = attrs.Factory(deque)
    lock: deque = attrs.Factory(deque)
    mode: int = None
 
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
        self.set_tile_mode(settings.soloviy.tiling_mode)
    
    @property
    def free(self) -> int:
        return len(self.order)
    
    @property
    def locked(self) -> int:
        return len(self.lock)

    @property    
    def free_space(self) -> bool:
        return self.locked < self.mode

    def tile_placed(self, playlist: str) -> Optional[PlaylistTile]:
        for pt in self.order + self.lock:
            if pt.playlist == playlist:
                return pt
        return None

    def set_tile_mode(self, mode: int):
        if mode in [1, 2, 3, 4]:
            self.mode = mode
        else:
            raise ValueError(f"Bad tiling mode: {mode}")
        
    def tile_add(self, playlist: str):
        if self.tile_placed(playlist):
            return
        elif self.free_space:
            if self.locked + self.free == self.mode: #TODO Move this to tiles_update
                pt_old = self.order.pop()
                self.tile_destroy(pt_old)
            pt_new = PlaylistTile(playlist)
            self.order.appendleft(pt_new)
        self.tile_layout_update.emit() # Update tiling
    
    def tile_destroy(self, tile: PlaylistTile):
        layout = self.layout()
        layout.removeWidget(tile)
        tile.deleteLater()
        if tile in self.lock:
            del self.lock[self.lock.index(tile)]
        if tile in self.order:
            del self.order[self.order.index(tile)]
    
    def tiles_update(self):
        layout = self.layout()
        for w,p in zip(self.lock + self.order,self.__get_tiling(self.free + self.locked)):
            layout.addWidget(w, *p)

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

#    async def add_tile(self, tile):
#        if self.locked + self.free == self.mode:
#            old_tile = self.order.pop()
#            await self.widget.playlist_destroy(old_tile, update=False, popped=True)
#        self.order.appendleft(tile)
#        await self.__update_tiling()
#    
#    async def destroy_tile(self, tile, update, popped):
#        if tile in self.lock:
#            del self.lock[self.lock.index(tile)]
#        elif not popped:
#            del self.order[self.order.index(tile)]
#        if update:
#            await self.__update_tiling()
#
#    async def lock_tile(self, tile):
#        del self.order[self.order.index(tile)]
#        self.lock.append(tile)
#        await self.__update_tiling()
#    
#    async def unlock_tile(self, tile):
#        del self.lock[self.lock.index(tile)]
#        self.order.appendleft(tile)
#        await self.__update_tiling()
#
#    async def __update_tiling(self):
#        layout = QGridLayout()
#        for w,p in zip(self.lock + self.order,self.__get_tiling(self.free + self.locked)):
#            layout.addWidget(w, *p)
#        if (old_layout := self.widget.layout()) is not None:
#            self.__delete_layout(old_layout)
#        self.widget.setLayout(layout)
#        self.__even_stretch(layout)
#
#    def __delete_layout(self, cur_lay):
#        if cur_lay is not None:
#            while cur_lay.count():
#                item = cur_lay.takeAt(0)
#                widget = item.widget()
#                if widget is not None:
#                    widget.deleteLater()
#                else:
#                    self.deleteLayout(item.layout())
#            sip.delete(cur_lay)
#    
#    def __get_tiling(self, count):
#        match count:
#            case 1:
#                return [(0,0,2,2)]
#            case 2:
#                return [(0,0,2,1),(0,1,2,1)]
#            case 3:
#                return [(0,0,2,1),(0,1,1,1),(1,1,1,1)]
#            case 4:
#                return [(0,0,1,1),(0,1,1,1),(1,0,1,1),(1,1,1,1)]
#            case _:
#                return ()
#    
#    def __even_stretch(self,layout):
#        layout.setColumnStretch(0,1)
#        layout.setColumnStretch(1,1)
#        layout.setRowStretch(0,1)
#        layout.setRowStretch(1,1)
#
#    def _init_connection(self, main):
#        self.main = main
#        self.tiler.set_tile_mode(self.main.config.get("tiling_mode"))
#
#    @staticmethod
#    def swappair2list(kv):
#        res = []
#        while kv:
#            chain = []
#            start,k = kv.popitem()
#            chain.append(start)
#            if start == k:
#                continue
#            while True:
#                v = kv.pop(k)
#                chain.append(k)
#                if v == start:
#                    break
#                k = v
#            res.append(chain)
#        return res
#
#    async def sort_playlist(self, kv):
#        lswap = self.swappair2list(kv)
#        for l in lswap:
#            for s1,s2 in itertools.pairwise(l):
#                await self.main.mpd.client.swap(s1,s2)
#    
#    async def fill_playlist(self, file_list):
#        for f in file_list:
#            await self.main.mpd.client.add(f)
#
#    async def add_playlist(self, playlist_name):
#        if self.tiler.free_space:
#            playlist = await self.main.mpd.client.listallinfo(playlist_name)
#            pt_new = PlaylistTile(self, playlist)
#            await self.tiler.add_tile(pt_new)
#
#    async def playlist_lock(self, pt, status):
#        if status:
#            await self.tiler.lock_tile(pt)
#        else:
#            await self.tiler.unlock_tile(pt)
#
#    async def playlist_destroy(self, pt, update=True, popped=False):
#        await self.tiler.destroy_tile(pt, update, popped)
#        if self.active_playlist is pt:
#            await self.main.mpd.client.clear()
#            await self.song_changed()
#            self.active_playlist = None
#
#    async def song_changed(self):
#        if song := await self.main.mpd.client.currentsong():
#            pos = int(song["pos"])
#            self.active_playlist.playlist_model.playing_status(pos)
#            index = self.active_playlist.playlist_model.index(pos, 0)
#            self.active_playlist.playlist_table.scrollTo(index,
#                    QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
#            song_row = self.active_playlist.playlist.iloc[pos]
#        else:
#            data = {
#                "title":"Unknown",
#                "artist":"Unknown",
#                "album":"Unknown",
#                "freq":"0",
#                "bitr":"0",
#                "chanels":"0",
#                "file": "Unknown.Unknown",
#            } 
#            song_row = pd.Series(data=data)
#        
#        asyncio.create_task(self.main._label_song_change(song_row))
#
#    async def playlist_song(self, tile, playlist, song_pos):
#        if self.active_playlist is not tile:
#            if self.active_playlist is not None:
#                self.active_playlist.playlist_model.playing_status()
#            await self.main.mpd.client.clear()
#            await asyncio.create_task(self.fill_playlist(
#                playlist["file"].to_list()))
#        await self.main.mpd.client.play(song_pos)
#        self.active_playlist = tile