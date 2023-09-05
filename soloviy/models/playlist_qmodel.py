from soloviy import db
from tinydb import Query
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QAbstractTableModel

PLAYING_ICON = QIcon.fromTheme("media-playback-start")
VISIBLE_COLUMNS = ["#", "file"]

class PlaylistModel(QAbstractTableModel):
    def __init__(self, playlist: str):
        super().__init__()
        self.playlist = playlist
        self.table = db.table(playlist)
        self.playing_id: int = None
        self.columns = VISIBLE_COLUMNS

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
        Song = Query()
        row = index.row()
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            entry = self.table.get(Song["#"] == row)
            column_name = self.columns[column]
            if column_name == "time":
                return self.strfdelta(entry.get(column_name))
            return str(entry.get(column_name))
#        if role == Qt.ItemDataRole.DecorationRole:
#            if self.playlist.at[row, "__playing"] and self.playlist.columns[column] == "#":
#                return PLAYING_ICON
    
    def rowCount(self, index):
        return len(self.table)
    
    def columnCount(self, index):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
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