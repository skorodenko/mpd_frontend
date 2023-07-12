import asyncio
import itertools
import pandas as pd
from ..utils.playlist_tiler import PlaylistTiler
from PyQt5 import QtWidgets
from .playlist_tile import PlaylistTile


class PTilingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_playlist = None
        self.tiler = PlaylistTiler(self)

    def _init_connection(self, main):
        self.main = main
        self.tiler.set_tile_mode(self.main.config.get("tiling_mode"))

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

    async def sort_playlist(self, kv):
        lswap = self.swappair2list(kv)
        for l in lswap:
            for s1,s2 in itertools.pairwise(l):
                await self.main.mpd.client.swap(s1,s2)
    
    async def fill_playlist(self, file_list):
        for f in file_list:
            await self.main.mpd.client.add(f)

    async def add_playlist(self, playlist_name):
        if self.tiler.free_space:
            playlist = await self.main.mpd.client.listallinfo(playlist_name)
            pt_new = PlaylistTile(self, playlist)
            await self.tiler.add_tile(pt_new)

    async def playlist_lock(self, pt, status):
        if status:
            await self.tiler.lock_tile(pt)
        else:
            await self.tiler.unlock_tile(pt)

    async def playlist_destroy(self, pt, update=True, popped=False):
        await self.tiler.destroy_tile(pt, update, popped)
        if self.active_playlist is pt:
            await self.main.mpd.client.clear()
            await self.song_changed()
            self.active_playlist = None

    async def song_changed(self):
        if song := await self.main.mpd.client.currentsong():
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
            await self.main.mpd.client.clear()
            await asyncio.create_task(self.fill_playlist(
                playlist["file"].to_list()))
        await self.main.mpd.client.play(song_pos)
        self.active_playlist = tile