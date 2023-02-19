from PyQt5 import QtWidgets
from collections import deque


class PTileWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = deque()

    def set_tiling(self, mode):
        if mode in ["1", "2", "3", "4"]:
            self.tmode = mode
        else:
            raise ValueError(f"Bad tiling mode: {mode}")