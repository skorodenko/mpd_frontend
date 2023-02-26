import soloviy.utils.time_utils as tu
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
            if self.playlist.columns[column] == "time":
                return tu.strfdelta(self.playlist.iloc[row, column])
            return str(self.playlist.iloc[row, column])
        if role == Qt.DecorationRole:
            if self.playlist.at[row, "__playing"] and column == 0:
                return PLAYING_ICON
    
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
        self.layoutAboutToBeChanged.emit()
        self.playlist["__playing"] = False
        if row is not None:
            self.playlist.at[row, "__playing"] = True
        self.layoutChanged.emit()

    def sort(self, section, order):
        self.layoutAboutToBeChanged.emit()
        self.playlist.sort_values(by=[self.playlist.columns[section]], 
                                    ascending=order, inplace=True)
        self.layoutChanged.emit()
    
    def reset_index(self):
        self.playlist.reset_index(drop=True, inplace=True)