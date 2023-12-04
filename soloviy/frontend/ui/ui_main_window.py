# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QListView,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QVBoxLayout,
    QWidget)

from soloviy.frontend.ui.custom_classes.jump_slider import JumpSlider
from soloviy.frontend.widgets.ptiling_widget import PTilingWidget
from . import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/logo.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionre = QAction(MainWindow)
        self.actionre.setObjectName(u"actionre")
        self.actiontest1 = QAction(MainWindow)
        self.actiontest1.setObjectName(u"actiontest1")
        self.actiontest1.setCheckable(True)
        self.actiontest1.setChecked(False)
        self.actiontest2 = QAction(MainWindow)
        self.actiontest2.setObjectName(u"actiontest2")
        self.actiontest2.setCheckable(True)
        self.actionDirectory = QAction(MainWindow)
        self.actionDirectory.setObjectName(u"actionDirectory")
        self.actionDirectory.setCheckable(True)
        self.actionFormat = QAction(MainWindow)
        self.actionFormat.setObjectName(u"actionFormat")
        self.actionFormat.setCheckable(True)
        self.actionArtist = QAction(MainWindow)
        self.actionArtist.setObjectName(u"actionArtist")
        self.actionArtist.setCheckable(True)
        self.actionAlbumartist = QAction(MainWindow)
        self.actionAlbumartist.setObjectName(u"actionAlbumartist")
        self.actionAlbumartist.setCheckable(True)
        self.actionAlbum = QAction(MainWindow)
        self.actionAlbum.setObjectName(u"actionAlbum")
        self.actionAlbum.setCheckable(True)
        self.actionDate = QAction(MainWindow)
        self.actionDate.setObjectName(u"actionDate")
        self.actionDate.setCheckable(True)
        self.actionGenre = QAction(MainWindow)
        self.actionGenre.setObjectName(u"actionGenre")
        self.actionGenre.setCheckable(True)
        self.actionComposer = QAction(MainWindow)
        self.actionComposer.setObjectName(u"actionComposer")
        self.actionComposer.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(False)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.playback_control = QHBoxLayout()
        self.playback_control.setSpacing(2)
        self.playback_control.setObjectName(u"playback_control")
        self.media_previous = QPushButton(self.layoutWidget)
        self.media_previous.setObjectName(u"media_previous")
        self.media_previous.setCursor(QCursor(Qt.ArrowCursor))
        self.media_previous.setAutoFillBackground(False)
        icon1 = QIcon()
        iconThemeName = u"media-skip-backward"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.media_previous.setIcon(icon1)
        self.media_previous.setIconSize(QSize(32, 32))
        self.media_previous.setAutoDefault(False)
        self.media_previous.setFlat(True)

        self.playback_control.addWidget(self.media_previous)

        self.media_play_pause = QPushButton(self.layoutWidget)
        self.media_play_pause.setObjectName(u"media_play_pause")
        self.media_play_pause.setAutoFillBackground(False)
        icon2 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.media_play_pause.setIcon(icon2)
        self.media_play_pause.setIconSize(QSize(32, 32))
        self.media_play_pause.setAutoDefault(False)
        self.media_play_pause.setFlat(True)

        self.playback_control.addWidget(self.media_play_pause)

        self.media_next = QPushButton(self.layoutWidget)
        self.media_next.setObjectName(u"media_next")
        self.media_next.setCursor(QCursor(Qt.ArrowCursor))
        self.media_next.setAutoFillBackground(False)
        icon3 = QIcon()
        iconThemeName = u"media-skip-forward"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.media_next.setIcon(icon3)
        self.media_next.setIconSize(QSize(32, 32))
        self.media_next.setCheckable(False)
        self.media_next.setAutoDefault(False)
        self.media_next.setFlat(True)

        self.playback_control.addWidget(self.media_next)


        self.horizontalLayout.addLayout(self.playback_control)

        self.horizontalSpacer_3 = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.playlist_control = QVBoxLayout()
        self.playlist_control.setSpacing(0)
        self.playlist_control.setObjectName(u"playlist_control")
        self.media_repeat = QPushButton(self.layoutWidget)
        self.media_repeat.setObjectName(u"media_repeat")
        self.media_repeat.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.media_repeat.sizePolicy().hasHeightForWidth())
        self.media_repeat.setSizePolicy(sizePolicy1)
        icon4 = QIcon()
        iconThemeName = u"media-playlist-repeat"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.media_repeat.setIcon(icon4)
        self.media_repeat.setIconSize(QSize(16, 16))
        self.media_repeat.setCheckable(False)
        self.media_repeat.setAutoRepeat(False)
        self.media_repeat.setFlat(True)

        self.playlist_control.addWidget(self.media_repeat)

        self.media_shuffle = QPushButton(self.layoutWidget)
        self.media_shuffle.setObjectName(u"media_shuffle")
        sizePolicy1.setHeightForWidth(self.media_shuffle.sizePolicy().hasHeightForWidth())
        self.media_shuffle.setSizePolicy(sizePolicy1)
        icon5 = QIcon()
        iconThemeName = u"media-playlist-shuffle"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.media_shuffle.setIcon(icon5)
        self.media_shuffle.setIconSize(QSize(16, 16))
        self.media_shuffle.setCheckable(False)
        self.media_shuffle.setFlat(True)

        self.playlist_control.addWidget(self.media_shuffle)


        self.horizontalLayout.addLayout(self.playlist_control)

        self.horizontalLayout.setStretch(1, 10)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.playlists_view = QListView(self.layoutWidget)
        self.playlists_view.setObjectName(u"playlists_view")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.playlists_view.sizePolicy().hasHeightForWidth())
        self.playlists_view.setSizePolicy(sizePolicy2)
        self.playlists_view.setFrameShape(QFrame.Box)
        self.playlists_view.setLineWidth(0)
        self.playlists_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.playlists_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.playlists_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.playlists_view.setAutoScroll(True)
        self.playlists_view.setAutoScrollMargin(0)
        self.playlists_view.setProperty("showDropIndicator", False)
        self.playlists_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlists_view.setIconSize(QSize(32, 32))
        self.playlists_view.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)

        self.verticalLayout.addWidget(self.playlists_view)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 9)
        self.splitter.addWidget(self.layoutWidget)
        self.ptiling_widget = PTilingWidget(self.splitter)
        self.ptiling_widget.setObjectName(u"ptiling_widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ptiling_widget.sizePolicy().hasHeightForWidth())
        self.ptiling_widget.setSizePolicy(sizePolicy3)
        self.splitter.addWidget(self.ptiling_widget)

        self.verticalLayout_2.addWidget(self.splitter)

        self.media_status = QHBoxLayout()
        self.media_status.setSpacing(4)
        self.media_status.setObjectName(u"media_status")
        self.label_art = QLabel(self.centralwidget)
        self.label_art.setObjectName(u"label_art")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_art.sizePolicy().hasHeightForWidth())
        self.label_art.setSizePolicy(sizePolicy4)
        self.label_art.setMinimumSize(QSize(64, 64))
        self.label_art.setMaximumSize(QSize(64, 64))
        self.label_art.setBaseSize(QSize(64, 64))
        self.label_art.setFrameShadow(QFrame.Sunken)
        self.label_art.setLineWidth(0)
        self.label_art.setScaledContents(True)
        self.label_art.setAlignment(Qt.AlignCenter)
        self.label_art.setMargin(0)
        self.label_art.setIndent(0)

        self.media_status.addWidget(self.label_art)

        self.media_progres = QVBoxLayout()
        self.media_progres.setSpacing(0)
        self.media_progres.setObjectName(u"media_progres")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)

        self.label_author = QLabel(self.centralwidget)
        self.label_author.setObjectName(u"label_author")

        self.gridLayout.addWidget(self.label_author, 1, 0, 1, 1)

        self.label_info = QLabel(self.centralwidget)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_info, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")
        self.label_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_time, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.media_progres.addLayout(self.gridLayout)

        self.media_seek = JumpSlider(self.centralwidget)
        self.media_seek.setObjectName(u"media_seek")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.media_seek.sizePolicy().hasHeightForWidth())
        self.media_seek.setSizePolicy(sizePolicy5)
        self.media_seek.setOrientation(Qt.Horizontal)

        self.media_progres.addWidget(self.media_seek)


        self.media_status.addLayout(self.media_progres)

        self.media_status.setStretch(1, 10)

        self.verticalLayout_2.addLayout(self.media_status)

        self.verticalLayout_2.setStretch(0, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 29))
        self.menubar.setDefaultUp(False)
        self.menu_Music = QMenu(self.menubar)
        self.menu_Music.setObjectName(u"menu_Music")
        self.menuGroup_by = QMenu(self.menu_Music)
        self.menuGroup_by.setObjectName(u"menuGroup_by")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_Music.menuAction())
        self.menu_Music.addAction(self.menuGroup_by.menuAction())
        self.menuGroup_by.addAction(self.actionDirectory)
        self.menuGroup_by.addAction(self.actionFormat)
        self.menuGroup_by.addAction(self.actionArtist)
        self.menuGroup_by.addAction(self.actionAlbumartist)
        self.menuGroup_by.addAction(self.actionAlbum)
        self.menuGroup_by.addAction(self.actionDate)
        self.menuGroup_by.addAction(self.actionGenre)
        self.menuGroup_by.addAction(self.actionComposer)

        self.retranslateUi(MainWindow)

        self.media_previous.setDefault(False)
        self.media_play_pause.setDefault(False)
        self.media_next.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionre.setText(QCoreApplication.translate("MainWindow", u"re", None))
        self.actiontest1.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.actiontest2.setText(QCoreApplication.translate("MainWindow", u"test2", None))
        self.actionDirectory.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.actionFormat.setText(QCoreApplication.translate("MainWindow", u"Format", None))
        self.actionArtist.setText(QCoreApplication.translate("MainWindow", u"Artist", None))
        self.actionAlbumartist.setText(QCoreApplication.translate("MainWindow", u"Albumartist", None))
        self.actionAlbum.setText(QCoreApplication.translate("MainWindow", u"Album", None))
        self.actionDate.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.actionGenre.setText(QCoreApplication.translate("MainWindow", u"Genre", None))
        self.actionComposer.setText(QCoreApplication.translate("MainWindow", u"Composer", None))
        self.media_previous.setText("")
        self.media_play_pause.setText("")
        self.media_next.setText("")
        self.media_repeat.setText("")
        self.media_shuffle.setText("")
        self.label_art.setText("")
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.label_author.setText(QCoreApplication.translate("MainWindow", u"Author", None))
        self.label_info.setText(QCoreApplication.translate("MainWindow", u"Format", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.menu_Music.setTitle(QCoreApplication.translate("MainWindow", u"&Music", None))
        self.menuGroup_by.setTitle(QCoreApplication.translate("MainWindow", u"Group by", None))
    # retranslateUi

