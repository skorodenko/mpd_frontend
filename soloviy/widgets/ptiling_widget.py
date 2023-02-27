import asyncio
import itertools
import pandas as pd
from PyQt5 import QtWidgets
from collections import deque
from ..windows.playlist_tile import PlaylistTile


class PTilingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = deque()
        self.lock = deque()
        self.layout = QtWidgets.QGridLayout()
        self.layout_tiles = deque()
        self.setLayout(self.layout)
        self.active_playlist = None

    async def _init_connection(self, main_window):
        self.main = main_window
        self.set_tiling(self.main.config.get("tiling_mode"))

    def set_tiling(self, mode):
        if mode in ["1", "2", "3", "4"]:
            self.tmode = int(mode)
            match self.tmode:
                case 1:
                    self.layout_tiles.appendleft((0,0,2,2))
                case 2:
                    self.layout_tiles.appendleft((0,0,2,1))
                    self.layout_tiles.appendleft((0,1,2,1))
                case 3:
                    self.layout_tiles.appendleft((0,0,2,1))
                    self.layout_tiles.appendleft((0,1,1,1))
                    self.layout_tiles.appendleft((1,1,1,1))
                case 4:
                    self.layout_tiles.appendleft((0,0,1,1))
                    self.layout_tiles.appendleft((0,1,1,1))
                    self.layout_tiles.appendleft((1,0,1,1))
                    self.layout_tiles.appendleft((1,1,1,1))
        else:
            raise ValueError(f"Bad tiling mode: {mode}")
    
    @staticmethod
    def swappair2list(kv):
        res = []
        while kv:
            chain = []
            start,k = kv.popitem()
            chain.append(start)
            if start == k:
                continue
            while True:
                v = kv.pop(k)
                chain.append(k)
                if v == start:
                    break
                k = v
            res.append(chain)
        return res

    async def fill_playlist(self, file_list):
        for f in file_list:
            await self.main.mpd_client.add(f)
    
    async def sort_playlist(self, kv):
        lswap = self.swappair2list(kv)
        for l in lswap:
            for s1,s2 in itertools.pairwise(l):
                await self.main.mpd_client.swap(s1,s2)

    def set_even_stretch(self):
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)
        self.layout.setRowStretch(0,1)
        self.layout.setRowStretch(1,1)

    async def add_playlist(self, playlist_name):
        l, o = len(self.lock), len(self.order)
        if l < self.tmode: 
            playlist = await self.main.mpd_client.listallinfo(playlist_name)
            if l + o == self.tmode:
                pt_old = self.order.pop()
                await self.playlist_destroy(pt_old, popped=True)
            tile = self.layout_tiles.pop()
            pt_new = PlaylistTile(self, playlist)
            pt_new.layout_tile = tile
            self.order.appendleft(pt_new)
            self.layout.addWidget(pt_new, *tile)
            self.set_even_stretch()

    async def playlist_lock(self, pt, status):
        if status:
            del self.order[self.order.index(pt)]
            self.lock.append(pt)
        else:
            del self.lock[self.lock.index(pt)]
            self.order.append(pt)

    async def playlist_destroy(self, pt, popped=False):
        if pt.lock_status:
            del self.lock[self.lock.index(pt)]
        elif not popped:
            del self.order[self.order.index(pt)]
        if self.active_playlist is pt:
            await self.main.mpd_client.clear()
            await self.song_changed()
            self.active_playlist = None
        tile = pt.layout_tile
        self.layout_tiles.appendleft(tile)
        self.layout.removeWidget(pt)

    async def song_changed(self):
        if song := await self.main.mpd_client.currentsong():
            pos = int(song["pos"])
            self.active_playlist.playlist_model.playing_status(pos)
            index = self.active_playlist.playlist_model.index(pos, 0)
            self.active_playlist.playlist_table.scrollTo(index,
                    QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
            song_row = self.active_playlist.playlist.iloc[pos]
        else:
            data = {
                "title":"Unknown",
                "artist":"Unknown",
                "album":"Unknown",
                "freq":"0",
                "bitr":"0",
                "chanels":"0",
                "file": "Unknown.Unknown",
            } 
            song_row = pd.Series(data=data)
        
        asyncio.create_task(self.main._label_song_change(song_row))

    async def playlist_song(self, tile, playlist, song_pos):
        if self.active_playlist is not tile:
            if self.active_playlist is not None:
                self.active_playlist.playlist_model.playing_status()
            await self.main.mpd_client.clear()
            await asyncio.create_task(self.fill_playlist(
                playlist["file"].to_list()))
        await self.main.mpd_client.play(song_pos)
        self.active_playlist = tile