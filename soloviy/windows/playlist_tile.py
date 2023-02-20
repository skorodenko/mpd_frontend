from ..widgets.ui_playlist_tile import Ui_Frame
from PyQt5 import QtWidgets


class PlaylistTile(QtWidgets.QFrame, Ui_Frame):
    def __init__(self, playlist):
        super().__init__()
        self.setupUi(self)
        self._playlist = playlist
        #TODO Connect buttons to ptiler
        match self._playlist:
            case [{"directory": title}, *etc]:
                self.playlist_title.setText(title)
        #TODO Create playlistmodel
    
    def test(self):
        ...