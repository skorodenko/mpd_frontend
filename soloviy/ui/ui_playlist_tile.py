# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playlist_tile.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.setWindowModality(Qt.WindowModal)
        Frame.resize(400, 300)
        Frame.setFrameShape(QFrame.StyledPanel)
        Frame.setFrameShadow(QFrame.Raised)
        Frame.setLineWidth(4)
        self.verticalLayout = QVBoxLayout(Frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.playlist_title = QLabel(Frame)
        self.playlist_title.setObjectName(u"playlist_title")

        self.horizontalLayout_2.addWidget(self.playlist_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.playlist_lock = QPushButton(Frame)
        self.playlist_lock.setObjectName(u"playlist_lock")
        icon = QIcon()
        iconThemeName = u"lock"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.playlist_lock.setIcon(icon)
        self.playlist_lock.setCheckable(True)
        self.playlist_lock.setFlat(True)

        self.horizontalLayout.addWidget(self.playlist_lock)

        self.playlist_destroy = QPushButton(Frame)
        self.playlist_destroy.setObjectName(u"playlist_destroy")
        icon1 = QIcon()
        iconThemeName = u"dialog-close"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.playlist_destroy.setIcon(icon1)
        self.playlist_destroy.setFlat(True)

        self.horizontalLayout.addWidget(self.playlist_destroy)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.playlist_table = QTableView(Frame)
        self.playlist_table.setObjectName(u"playlist_table")
        self.playlist_table.setFocusPolicy(Qt.NoFocus)
        self.playlist_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist_table.setFrameShape(QFrame.NoFrame)
        self.playlist_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.playlist_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.playlist_table.setAutoScrollMargin(0)
        self.playlist_table.setProperty("showDropIndicator", False)
        self.playlist_table.setDragDropOverwriteMode(True)
        self.playlist_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playlist_table.setTextElideMode(Qt.ElideLeft)
        self.playlist_table.setShowGrid(False)
        self.playlist_table.setSortingEnabled(True)
        self.playlist_table.setWordWrap(True)
        self.playlist_table.setCornerButtonEnabled(False)
        self.playlist_table.horizontalHeader().setCascadingSectionResizes(False)
        self.playlist_table.horizontalHeader().setStretchLastSection(True)
        self.playlist_table.verticalHeader().setVisible(False)
        self.playlist_table.verticalHeader().setMinimumSectionSize(20)
        self.playlist_table.verticalHeader().setDefaultSectionSize(24)
        self.playlist_table.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.playlist_table)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.playlist_title.setText(QCoreApplication.translate("Frame", u"PlaylistTitle", None))
        self.playlist_lock.setText("")
        self.playlist_destroy.setText("")
    # retranslateUi

