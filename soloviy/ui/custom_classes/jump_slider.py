from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal


class JumpSlider(QtWidgets.QSlider):
    pressed = pyqtSignal(int)
    dragged = pyqtSignal(int)
    released = pyqtSignal(int)

    def __init__(self, parent=None):
        super(JumpSlider, self).__init__(parent)
        self.__pressed = False

    def __setPosVal(self, event):
        value = QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), int(event.x()), self.width())
        self.setValue(value)
        return value

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.__pressed = True
            e.accept()
            value = self.__setPosVal(e)
            self.pressed.emit(value)

    def mouseMoveEvent(self, e):
        if self.__pressed:
            e.accept()
            value = self.__setPosVal(e)
            self.dragged.emit(value)
        return super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.__pressed = False
            e.accept()
            value = self.__setPosVal(e)
            self.released.emit(value)
        self.sliderMoved.emit(value)
        return super().mouseReleaseEvent(e)