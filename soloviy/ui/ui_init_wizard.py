# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'init_wizard.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget, QWizard, QWizardPage)
from . import icons_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.setWindowModality(Qt.WindowModal)
        Wizard.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/icons/logo.svg", QSize(), QIcon.Normal, QIcon.Off)
        Wizard.setWindowIcon(icon)
        Wizard.setWizardStyle(QWizard.ModernStyle)
        Wizard.setOptions(QWizard.NoBackButtonOnLastPage|QWizard.NoBackButtonOnStartPage|QWizard.NoCancelButtonOnLastPage)
        Wizard.setTitleFormat(Qt.AutoText)
        self.wizardStart = QWizardPage()
        self.wizardStart.setObjectName(u"wizardStart")
        self.wizardStart.setAutoFillBackground(False)
        Wizard.setPage(1, self.wizardStart)
        self.wizardMPDConfig = QWizardPage()
        self.wizardMPDConfig.setObjectName(u"wizardMPDConfig")
        self.verticalLayout_2 = QVBoxLayout(self.wizardMPDConfig)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.wizardMPDConfig)
        self.label.setObjectName(u"label")
        self.label.setMouseTracking(True)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mpd_socket_type = QComboBox(self.wizardMPDConfig)
        self.mpd_socket_type.addItem("")
        self.mpd_socket_type.addItem("")
        self.mpd_socket_type.setObjectName(u"mpd_socket_type")

        self.verticalLayout.addWidget(self.mpd_socket_type)

        self.mpd_socket = QLineEdit(self.wizardMPDConfig)
        self.mpd_socket.setObjectName(u"mpd_socket")
        self.mpd_socket.setEnabled(False)
        self.mpd_socket.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.mpd_socket)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.alert = QWidget(self.wizardMPDConfig)
        self.alert.setObjectName(u"alert")
        self.alert.setMinimumSize(QSize(0, 0))
        self.alert.setMaximumSize(QSize(16777215, 0))
        self.alert.setBaseSize(QSize(0, 0))
        self.horizontalLayout_3 = QHBoxLayout(self.alert)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.alert_text = QLabel(self.alert)
        self.alert_text.setObjectName(u"alert_text")

        self.horizontalLayout_3.addWidget(self.alert_text)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.alert)

        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 3)
        self.verticalLayout_2.setStretch(3, 2)
        Wizard.addPage(self.wizardMPDConfig)
        self.wizardFinish = QWizardPage()
        self.wizardFinish.setObjectName(u"wizardFinish")
        self.verticalLayout_3 = QVBoxLayout(self.wizardFinish)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(self.wizardFinish)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        Wizard.addPage(self.wizardFinish)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Initial config", None))
        self.wizardStart.setTitle(QCoreApplication.translate("Wizard", u"Soloviy", None))
        self.wizardStart.setSubTitle(QCoreApplication.translate("Wizard", u"Inital app configuration", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:14pt;\">Choose mpd socket to use</span></p></body></html>", None))
        self.mpd_socket_type.setItemText(0, QCoreApplication.translate("Wizard", u"Built-in", None))
        self.mpd_socket_type.setItemText(1, QCoreApplication.translate("Wizard", u"External", None))

        self.mpd_socket.setInputMask("")
        self.mpd_socket.setText("")
        self.mpd_socket.setPlaceholderText(QCoreApplication.translate("Wizard", u"Enter mpd socket", None))
        self.alert_text.setText("")
        self.label_2.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:14pt;\">Finished initial configuration</span></p></body></html>", None))
    # retranslateUi

