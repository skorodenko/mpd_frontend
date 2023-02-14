from PyQt6 import QtWidgets


class JumpSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(JumpSlider, self).__init__(parent)
        self.setTracking(False)
        self.setSingleStep(1)

    def mousePressEvent(self, event):
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), int(event.position().x()), self.width()))

    def mouseMoveEvent(self, event):
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), int(event.position().x()), self.width()))