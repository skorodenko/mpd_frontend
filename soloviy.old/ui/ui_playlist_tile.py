# Form implementation generated from reading ui file 'soloviy/ui/templates/playlist_tile.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        Frame.resize(400, 300)
        Frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        Frame.setLineWidth(4)
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.playlist_title = QtWidgets.QLabel(parent=Frame)
        self.playlist_title.setObjectName("playlist_title")
        self.horizontalLayout_2.addWidget(self.playlist_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playlist_lock = QtWidgets.QPushButton(parent=Frame)
        self.playlist_lock.setText("")
        icon = QtGui.QIcon.fromTheme("lock")
        self.playlist_lock.setIcon(icon)
        self.playlist_lock.setCheckable(True)
        self.playlist_lock.setFlat(True)
        self.playlist_lock.setObjectName("playlist_lock")
        self.horizontalLayout.addWidget(self.playlist_lock)
        self.playlist_destroy = QtWidgets.QPushButton(parent=Frame)
        self.playlist_destroy.setText("")
        icon = QtGui.QIcon.fromTheme("dialog-close")
        self.playlist_destroy.setIcon(icon)
        self.playlist_destroy.setFlat(True)
        self.playlist_destroy.setObjectName("playlist_destroy")
        self.horizontalLayout.addWidget(self.playlist_destroy)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.playlist_table = QtWidgets.QTableView(parent=Frame)
        self.playlist_table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.playlist_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlist_table.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.playlist_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.playlist_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.playlist_table.setAutoScrollMargin(0)
        self.playlist_table.setProperty("showDropIndicator", False)
        self.playlist_table.setDragDropOverwriteMode(True)
        self.playlist_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.playlist_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.playlist_table.setTextElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.playlist_table.setShowGrid(False)
        self.playlist_table.setSortingEnabled(True)
        self.playlist_table.setWordWrap(True)
        self.playlist_table.setCornerButtonEnabled(False)
        self.playlist_table.setObjectName("playlist_table")
        self.playlist_table.horizontalHeader().setCascadingSectionResizes(False)
        self.playlist_table.horizontalHeader().setStretchLastSection(True)
        self.playlist_table.verticalHeader().setVisible(False)
        self.playlist_table.verticalHeader().setDefaultSectionSize(24)
        self.playlist_table.verticalHeader().setHighlightSections(False)
        self.playlist_table.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout.addWidget(self.playlist_table)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.playlist_title.setText(_translate("Frame", "PlaylistTitle"))