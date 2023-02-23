import asyncio
from PyQt5 import QtWidgets
from collections import deque
import itertools
from ..windows.playlist_tile import PlaylistTile


class PTilingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = deque()
        self.lock = deque()
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.active_playlist = None

    async def _init_connection(self, main_window):
        self.main = main_window
        self.set_tiling(self.main.config.get("tiling_mode"))

    def set_tiling(self, mode):
        if mode in ["1", "2", "3", "4"]:
            self.tmode = int(mode)
        else:
            raise ValueError(f"Bad tiling mode: {mode}")
    
    def set_even_stretch(self):
        l, o = len(self.lock), len(self.order)
        for i in range(l+o):
            self.layout.setStretch(i, 1)

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

    async def add_playlist(self, playlist_name):
        l, o = len(self.lock), len(self.order)
        if l < self.tmode: 
            playlist = await self.main.mpd_client.listallinfo(playlist_name)
            if l + o == self.tmode:
                pt_old = self.order.pop()
                await self.playlist_destroy(pt_old, popped=True)
            pt_new = PlaylistTile(self, playlist)
            self.order.appendleft(pt_new)
            self.layout.addWidget(pt_new)
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
            self.active_playlist = None
        self.layout.removeWidget(pt)

    async def song_changed(self):
        if song := await self.main.mpd_client.currentsong():
            self.active_playlist.playlist_model.playing_status(int(song["pos"]))

    async def playlist_song(self, tile, playlist, song_pos):
        if self.active_playlist is not tile:
            await self.main.mpd_client.clear()
            await asyncio.create_task(self.fill_playlist(
                playlist["file"].to_list()))
        await self.main.mpd_client.play(song_pos)
        self.active_playlist = tile