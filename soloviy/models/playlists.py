from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractListModel, Qt


FOLDER_ICON = QIcon.fromTheme("folder-music")

class PlaylistsModel(QAbstractListModel):
    def __init__(self, playlists):
        super().__init__()
        self.playlists = [
            playlist["directory"] for playlist in playlists
            if not playlist.get("directory", ".").startswith(".")
        ]
        self.playlists.sort()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            name = self.playlists[index.row()]
            return name
        if role == Qt.ItemDataRole.DecorationRole:
            return FOLDER_ICON
    
    def rowCount(self, index):
        return len(self.playlists)