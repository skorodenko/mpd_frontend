import asyncio
from PyQt5 import QtWidgets
from collections import deque
from ..windows.playlist_tile import PlaylistTile


class PTilingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = deque()
        self.lock = deque()
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def _init_connection(self, main_window):
        self.main = main_window
        self.set_tiling(self.main.config.get("tiling_mode"))

    def set_tiling(self, mode):
        if mode in ["1", "2", "3", "4"]:
            self.tmode = int(mode)
        else:
            raise ValueError(f"Bad tiling mode: {mode}")
        
    async def fill_playlist(self, file_list):
        for f in file_list:
            await self.main.mpd_client.add(f)    
    
    async def add_playlist(self, playlist_name):
        if len(self.lock) < self.tmode: 
            playlist = await self.main.mpd_client.listallinfo(playlist_name)
            if len(self.lock) + len(self.order) == self.tmode:
                pt_old = self.order.pop()
                await self.playlist_destroy(pt_old, popped=True)
            pt_new = PlaylistTile(self, playlist)
            self.order.appendleft(pt_new)
            self.layout.addWidget(pt_new)

    async def playlist_destroy(self, pt, popped=False):
        if not popped:
            del self.order[self.order.index(pt)]
        await self.main.mpd_client.clear()
        self.layout.removeWidget(pt)
    
    async def playlist_song(self, playlist, song_pos):
        await self.main.mpd_client.clear()
        await asyncio.create_task(self.fill_playlist(
            playlist["file"].to_list()))
        await self.main.mpd_client.play(song_pos)