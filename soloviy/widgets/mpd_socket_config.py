from PyQt5 import QtWidgets, QtCore
from ..ui.ui_mpd_socket_config import Ui_Dialog
from ..constants import MPD_NATIVE_SOCKET



class MpdSocketConfig(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, main):
        super().__init__(main)
        self.setupUi(self)
        self.main = main
        self.logo.load("logo:logo.svg")

        self.mpd_socket_type.currentIndexChanged.connect(self.__socket_type_combo_box)
        self.accepted.connect(self.__connect_mpd)

    def __socket_type_combo_box(self):
        if self.mpd_socket.isEnabled():
            self.mpd_socket.setEnabled(False)
        else:
            self.mpd_socket.setEnabled(True)

    def __connect_mpd(self):
        match self.mpd_socket_type.currentText():
            case "Built-in":
                self.main.config.set("mpd_socket", MPD_NATIVE_SOCKET)
            case "External":
                new_external_socket = self.mpd_socket.text()
                self.main.config.set("mpd_socket", new_external_socket)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtCore.QDir.addSearchPath("logo", "./soloviy/resources/logo/")        
    Dialog = QtWidgets.QDialog()
    ui = MpdSocketConfig(Dialog)
    Dialog.show()
    sys.exit(app.exec())