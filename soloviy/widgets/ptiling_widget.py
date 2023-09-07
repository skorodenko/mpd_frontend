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
    
    def _bind_tile_signals(self, tile: PlaylistTile):
        tile.lock.connect(
            self.__manage_tile_lock
        )
        tile.destroy.connect(
            self.__manage_tile_destruction
        )
    
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
            self._bind_tile_signals(pt_new)
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
            case _:
                return []
    
    def __manage_tile_lock(self, tile: PlaylistTile, locked: bool):
        if locked: #-> unlock
            del self.order[self.order.index(tile)]
            self.lock.append(tile)
        else: #-> lock
            del self.lock[self.lock.index(tile)]
            self.order.appendleft(tile)
        self.tile_layout_update.emit()
    
    def __manage_tile_destruction(self, tile: PlaylistTile):
        self.tile_destroy(tile)
        self.tile_layout_update.emit()

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