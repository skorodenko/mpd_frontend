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

    def set_tiling(self, mode):
        if mode in ["1", "2", "3", "4"]:
            self.tmode = mode
        else:
            raise ValueError(f"Bad tiling mode: {mode}")
    
    async def add_playlist(self, playlist_name):
        playlist = await self.main.mpd_client.listallinfo(playlist_name)
        print(playlist)
        a = PlaylistTile(playlist)
        #a.test()
        self.layout.addWidget(a)
        ...