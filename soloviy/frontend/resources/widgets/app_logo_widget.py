from PyQt6 import QtSvgWidgets

LOGO_PATH="./resources/logo/64/logo.svg"

class AppLogoWidget(QtSvgWidgets.QSvgWidget):
    def __init__(self, parent=None, file=LOGO_PATH):
        super(AppLogoWidget, self).__init__(file, parent)