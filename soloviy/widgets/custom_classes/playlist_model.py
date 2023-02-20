from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

class PlaylistModel(QtCore.QAbstractTableModel):
    def __init__(self, playlist):
        super().__init__()
        ...

    def data(self, index, role):
        ...
    
    def rowCount(self, index):
        ...
    
    def columnCount(self, index):
        ...
    
    def headerData(self, section, orientation, role):
        ...