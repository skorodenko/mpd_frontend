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
            return str(self.playlist.iloc[row, column])
    
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
            
    def sort(self, section, order):
        try:
            self.layoutAboutToBeChanged.emit()
            self.playlist.sort_values(by=[self.playlist.columns[section]], 
                                        ascending=order, inplace=True)
            self.layoutChanged.emit()
        except Exception as e:
            raise e
    
    def reset_index(self):
        self.playlist.reset_index(drop=True, inplace=True)