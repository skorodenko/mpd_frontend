import qtinter
from ..widgets.ui_playlist_tile import Ui_Frame
from PyQt5 import QtWidgets, QtCore
from ..widgets.custom_classes.playlist_model import PlaylistModel
import pandas as pd


class PlaylistTile(QtWidgets.QFrame, Ui_Frame):
    def __init__(self, tiler, playlist):
        super().__init__()
        self.setupUi(self)
        self.tiler = tiler
        #TODO Connect buttons to ptiler
        match playlist:
            case [{"directory": title}, *etc]:
                self.title = title
                self.playlist = [d for d in etc if d.get("file") is not None]
                self.playlist = pd.DataFrame.from_dict(self.playlist)
        self.playlist_title.setText(self.title)
        self.playlist_model = PlaylistModel(self.playlist)
        self.playlist_table.setModel(self.playlist_model)
        
        self.playlist_table.doubleClicked.connect(
            qtinter.asyncslot(self.play_song)
        )
        self.playlist_destroy.clicked.connect(
            qtinter.asyncslot(self.destroy)
        )

    async def play_song(self, index):
        tile = self
        playlist = self.playlist_model.playlist
        song_pos = index.row()
        await self.tiler.playlist_song(tile, playlist, song_pos)

    async def destroy(self):
        await self.tiler.playlist_destroy(self)