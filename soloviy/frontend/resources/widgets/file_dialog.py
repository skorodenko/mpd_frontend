from PyQt6 import QtWidgets


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__(parent)