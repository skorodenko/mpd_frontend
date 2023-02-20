# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'soloviy/resources/templates/playlist_tile.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.setWindowModality(QtCore.Qt.WindowModal)
        Frame.resize(400, 300)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        Frame.setLineWidth(4)
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.playlist_title = QtWidgets.QLabel(Frame)
        self.playlist_title.setObjectName("playlist_title")
        self.horizontalLayout_2.addWidget(self.playlist_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playlist_pin = QtWidgets.QPushButton(Frame)
        self.playlist_pin.setText("")
        icon = QtGui.QIcon.fromTheme("lock")
        self.playlist_pin.setIcon(icon)
        self.playlist_pin.setCheckable(True)
        self.playlist_pin.setFlat(True)
        self.playlist_pin.setObjectName("playlist_pin")
        self.horizontalLayout.addWidget(self.playlist_pin)
        self.playlist_close = QtWidgets.QPushButton(Frame)
        self.playlist_close.setText("")
        icon = QtGui.QIcon.fromTheme("dialog-close")
        self.playlist_close.setIcon(icon)
        self.playlist_close.setFlat(True)
        self.playlist_close.setObjectName("playlist_close")
        self.horizontalLayout.addWidget(self.playlist_close)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.playlist_table = QtWidgets.QTableWidget(Frame)
        self.playlist_table.setObjectName("playlist_table")
        self.playlist_table.setColumnCount(0)
        self.playlist_table.setRowCount(0)
        self.playlist_table.verticalHeader().setVisible(False)
        self.playlist_table.verticalHeader().setHighlightSections(False)
        self.verticalLayout.addWidget(self.playlist_table)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.playlist_title.setText(_translate("Frame", "PlaylistTitle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
