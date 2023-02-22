from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

PLAYING_ICON = QtGui.QIcon.fromTheme("media-playback-start")

class PlaylistModel(QtCore.QAbstractTableModel):
    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist

    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            match (row, column):
                case row, None:
                    return self.playlist.iloc[[row]]
                case row, column:
                    return str(self.playlist.iloc[row, column])
        if role == Qt.DecorationRole:
            if self.playlist.at[row, "__playing"] and column == 0:
                return PLAYING_ICON
        if role == Qt.TextAlignmentRole:
            if column == 0:
                return Qt.AlignCenter
    
    def rowCount(self, index):
        rows, _ = self.playlist.shape
        return rows
    
    def columnCount(self, index):
        _, columns = self.playlist.shape
        return columns
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.playlist.columns[section]
            
    def playing_status(self, row=None):
        try:
            self.layoutAboutToBeChanged.emit()
            self.playlist["__playing"] = False
            if row is not None:
                self.playlist.at[row, "__playing"] = True
            self.layoutChanged.emit()
        except Exception as e:
            raise e

    def sort(self, section, order):
        try:
            self.layoutAboutToBeChanged.emit()
            self.playlist = self.playlist.sort_values(self.playlist.columns[section], ascending=order)
            self.layoutChanged.emit()
        except Exception as e:
            ...
    
    def headerClicked(self, section, order):
        self.sort(section, bool(order))