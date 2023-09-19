from soloviy.models.dbmodels import PlaylistTile, Playlist
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QAbstractTableModel, QAbstractListModel

FOLDER_ICON = QIcon.fromTheme("folder-music")
PLAYING_ICON = QIcon.fromTheme("media-playback-start")
VISIBLE_COLUMNS = ["track", "file"] # Move to config

class PlaylistModel(QAbstractTableModel):
    def __init__(self, playlist: str):
        super().__init__()
        self.playlist = playlist
        self.columns = VISIBLE_COLUMNS
        self._query = Playlist.select().where(Playlist.playlist_name == self.playlist)
        
    @property
    def query(self):
        return self._query

    @staticmethod
    def strfdelta(tdelta):
        h, rem = divmod(tdelta, 3600)
        m, s = divmod(rem, 60)
        match h,m,s:
            case h,_,_ if h != 0:
                return f"{h}:{m:0>2}:{s:0>2}"
            case _:
                return f"{m:0>2}:{s:0>2}"
    
    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            column_name = self.columns[column]
            #if column_name == "time":
            #    return self.strfdelta(entry.get(column_name))
            return str(getattr(self.query[row], column_name))
#        if role == Qt.ItemDataRole.DecorationRole:
#            if self.playlist.at[row, "__playing"] and self.playlist.columns[column] == "#":
#                return PLAYING_ICON
    
    def rowCount(self, index):
        return Playlist.select().where(Playlist.playlist_name == self.playlist).count()
    
    def columnCount(self, index):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == self.columns.index("track"):
                    return "#"
                return self.columns[section]
    
#    def playing_status(self, row=None):
#        self.layoutAboutToBeChanged.emit()
#        self.playlist["__playing"] = False
#        if row is not None:
#            self.playlist.at[row, "__playing"] = True
#        self.layoutChanged.emit()
#
#    def sort(self, section, order):
#        self.layoutAboutToBeChanged.emit()
#        self.playlist.sort_values(by=[self.playlist.columns[section]], 
#                                    ascending=order, inplace=True)
#        self.layoutChanged.emit()
#    
#    def reset_index(self):
#        self.playlist.reset_index(drop=True, inplace=True)


class PlaylistsModel(QAbstractListModel):
    def __init__(self, playlists):
        super().__init__()
        self.playlists = playlists

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            name = self.playlists[index.row()]
            return name
        if role == Qt.ItemDataRole.DecorationRole:
            return FOLDER_ICON
    
    def rowCount(self, index):
        return len(self.playlists)