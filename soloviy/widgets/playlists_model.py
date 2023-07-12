from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

FOLDER_ICON = QtGui.QIcon.fromTheme("folder-music")

class PlaylistsModel(QtCore.QAbstractListModel):
    def __init__(self, playlists):
        super().__init__()
        self.playlists = [
            playlist["directory"] for playlist in playlists
            if not playlist.get("directory", ".").startswith(".")
        ]
        self.playlists.sort()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            name = self.playlists[index.row()]
            return name
        if role == Qt.DecorationRole:
            return FOLDER_ICON
    
    def rowCount(self, index):
        return len(self.playlists)