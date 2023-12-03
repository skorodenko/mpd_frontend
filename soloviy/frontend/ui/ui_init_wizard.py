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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget, QWizard, QWizardPage)
from . import icons_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.setWindowModality(Qt.WindowModal)
        Wizard.resize(581, 448)
        icon = QIcon()
        icon.addFile(u":/icons/logo.svg", QSize(), QIcon.Normal, QIcon.Off)
        Wizard.setWindowIcon(icon)
        Wizard.setWizardStyle(QWizard.ModernStyle)
        Wizard.setOptions(QWizard.IndependentPages|QWizard.NoBackButtonOnLastPage|QWizard.NoBackButtonOnStartPage|QWizard.NoCancelButtonOnLastPage)
        Wizard.setTitleFormat(Qt.AutoText)
        self.wizardStart = QWizardPage()
        self.wizardStart.setObjectName(u"wizardStart")
        self.wizardStart.setAutoFillBackground(False)
        self.verticalLayout_4 = QVBoxLayout(self.wizardStart)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.label_4 = QLabel(self.wizardStart)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.frame = QFrame(self.wizardStart)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_7 = QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.radio_server = QRadioButton(self.frame)
        self.radio_server.setObjectName(u"radio_server")

        self.verticalLayout_7.addWidget(self.radio_server)

        self.radio_server_text = QLabel(self.frame)
        self.radio_server_text.setObjectName(u"radio_server_text")
        self.radio_server_text.setScaledContents(False)
        self.radio_server_text.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.radio_server_text)

        self.radio_local = QRadioButton(self.frame)
        self.radio_local.setObjectName(u"radio_local")
        self.radio_local.setEnabled(False)

        self.verticalLayout_7.addWidget(self.radio_local)

        self.radio_local_text = QLabel(self.frame)
        self.radio_local_text.setObjectName(u"radio_local_text")
        self.radio_local_text.setEnabled(False)
        self.radio_local_text.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.radio_local_text)


        self.verticalLayout_4.addWidget(self.frame)

        self.verticalSpacer_5 = QSpacerItem(20, 76, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.wizardStart_alert = QWidget(self.wizardStart)
        self.wizardStart_alert.setObjectName(u"wizardStart_alert")
        sizePolicy.setHeightForWidth(self.wizardStart_alert.sizePolicy().hasHeightForWidth())
        self.wizardStart_alert.setSizePolicy(sizePolicy)
        self.wizardStart_alert.setMinimumSize(QSize(0, 0))
        self.wizardStart_alert.setMaximumSize(QSize(16777215, 0))
        self.wizardStart_alert.setBaseSize(QSize(0, 0))
        self.horizontalLayout_9 = QHBoxLayout(self.wizardStart_alert)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_17)

        self.wizardStart_alert_text = QLabel(self.wizardStart_alert)
        self.wizardStart_alert_text.setObjectName(u"wizardStart_alert_text")
        sizePolicy.setHeightForWidth(self.wizardStart_alert_text.sizePolicy().hasHeightForWidth())
        self.wizardStart_alert_text.setSizePolicy(sizePolicy)

        self.horizontalLayout_9.addWidget(self.wizardStart_alert_text)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_18)


        self.verticalLayout_4.addWidget(self.wizardStart_alert)

        Wizard.setPage(1, self.wizardStart)
        self.wizardLocalConfig = QWizardPage()
        self.wizardLocalConfig.setObjectName(u"wizardLocalConfig")
        self.verticalLayout = QVBoxLayout(self.wizardLocalConfig)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.label_8 = QLabel(self.wizardLocalConfig)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

        self.label_5 = QLabel(self.wizardLocalConfig)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.frame_3 = QFrame(self.wizardLocalConfig)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Sunken)
        self.formLayout_2 = QFormLayout(self.frame_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_12 = QLabel(self.frame_3)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_12)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.wizardLocalConfig_musicfolder_text = QLineEdit(self.frame_3)
        self.wizardLocalConfig_musicfolder_text.setObjectName(u"wizardLocalConfig_musicfolder_text")
        self.wizardLocalConfig_musicfolder_text.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.wizardLocalConfig_musicfolder_text)

        self.wizardLocalConfig_filedialog = QPushButton(self.frame_3)
        self.wizardLocalConfig_filedialog.setObjectName(u"wizardLocalConfig_filedialog")
        icon1 = QIcon(QIcon.fromTheme(u"folder"))
        self.wizardLocalConfig_filedialog.setIcon(icon1)
        self.wizardLocalConfig_filedialog.setIconSize(QSize(20, 20))
        self.wizardLocalConfig_filedialog.setFlat(True)

        self.horizontalLayout_2.addWidget(self.wizardLocalConfig_filedialog)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.frame_3)

        self.verticalSpacer_2 = QSpacerItem(20, 272, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.wizardLocalConfig_alert = QWidget(self.wizardLocalConfig)
        self.wizardLocalConfig_alert.setObjectName(u"wizardLocalConfig_alert")
        self.wizardLocalConfig_alert.setMinimumSize(QSize(0, 0))
        self.wizardLocalConfig_alert.setMaximumSize(QSize(16777215, 0))
        self.wizardLocalConfig_alert.setBaseSize(QSize(0, 0))
        self.horizontalLayout_8 = QHBoxLayout(self.wizardLocalConfig_alert)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_15)

        self.wizardLocalConfig_alert_text = QLabel(self.wizardLocalConfig_alert)
        self.wizardLocalConfig_alert_text.setObjectName(u"wizardLocalConfig_alert_text")

        self.horizontalLayout_8.addWidget(self.wizardLocalConfig_alert_text)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_16)


        self.verticalLayout.addWidget(self.wizardLocalConfig_alert)

        Wizard.addPage(self.wizardLocalConfig)
        self.wizardServerConfig = QWizardPage()
        self.wizardServerConfig.setObjectName(u"wizardServerConfig")
        self.verticalLayout_2 = QVBoxLayout(self.wizardServerConfig)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.wizardServerConfig)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.label_3 = QLabel(self.wizardServerConfig)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.frame_2 = QFrame(self.wizardServerConfig)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.formLayout = QFormLayout(self.frame_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.wizardServerConfig_host = QLineEdit(self.frame_2)
        self.wizardServerConfig_host.setObjectName(u"wizardServerConfig_host")
        self.wizardServerConfig_host.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.wizardServerConfig_host)

        self.wizardServerConfig_port = QSpinBox(self.frame_2)
        self.wizardServerConfig_port.setObjectName(u"wizardServerConfig_port")
        self.wizardServerConfig_port.setMaximum(9999999)
        self.wizardServerConfig_port.setValue(6600)

        self.horizontalLayout.addWidget(self.wizardServerConfig_port)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.wizardServerConfig_password = QLineEdit(self.frame_2)
        self.wizardServerConfig_password.setObjectName(u"wizardServerConfig_password")
        self.wizardServerConfig_password.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.wizardServerConfig_password)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.wizardServerConfig_alert = QWidget(self.wizardServerConfig)
        self.wizardServerConfig_alert.setObjectName(u"wizardServerConfig_alert")
        self.wizardServerConfig_alert.setMinimumSize(QSize(0, 0))
        self.wizardServerConfig_alert.setMaximumSize(QSize(16777215, 0))
        self.wizardServerConfig_alert.setBaseSize(QSize(0, 0))
        self.horizontalLayout_6 = QHBoxLayout(self.wizardServerConfig_alert)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_11)

        self.wizardServerConfig_alert_text = QLabel(self.wizardServerConfig_alert)
        self.wizardServerConfig_alert_text.setObjectName(u"wizardServerConfig_alert_text")

        self.horizontalLayout_6.addWidget(self.wizardServerConfig_alert_text)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_12)


        self.verticalLayout_2.addWidget(self.wizardServerConfig_alert)

        Wizard.addPage(self.wizardServerConfig)
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

        self.wizardLocalConfig_filedialog.setDefault(False)


        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Initial config", None))
        self.wizardStart.setTitle(QCoreApplication.translate("Wizard", u"Soloviy", None))
        self.wizardStart.setSubTitle(QCoreApplication.translate("Wizard", u"Inital app configuration", None))
        self.label_4.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:12pt;\">Please select how you would like to connect to mpd:</span></p></body></html>", None))
        self.radio_server.setText(QCoreApplication.translate("Wizard", u"Server mpd setup", None))
        self.radio_server_text.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-style:italic;\">Choose this option if you have already have running and properly configured mpd server and/or if you want to be able to connect to this server from other clients.</span></p></body></html>", None))
        self.radio_local.setText(QCoreApplication.translate("Wizard", u"Local mpd setup", None))
        self.radio_local_text.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-style:italic;\">Choose this option if your music collection is located on this machine and you </span><span style=\" font-weight:700; text-decoration: underline;\">have mpd binary installed (available on PATH)</span><span style=\" font-style:italic;\">. This server will be running on Soloviy startup. Please note that you won't be able to access this server from any other client.</span></p></body></html>", None))
        self.wizardStart_alert_text.setText("")
        self.label_8.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:14pt;\">Local mpd setup</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Please enter the location of your music collection and click 'Next' button</p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("Wizard", u"Music folder:", None))
        self.wizardLocalConfig_musicfolder_text.setText("")
        self.wizardLocalConfig_filedialog.setText("")
        self.wizardLocalConfig_alert_text.setText("")
        self.label.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:14pt;\">Server mpd connection setup</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Please enter the relevant details and click 'Next' button</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Wizard", u"Host:", None))
        self.wizardServerConfig_host.setText("")
        self.label_7.setText(QCoreApplication.translate("Wizard", u"Password:", None))
        self.wizardServerConfig_password.setText("")
        self.wizardServerConfig_alert_text.setText("")
        self.label_2.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p><span style=\" font-size:14pt;\">Finished initial configuration</span></p></body></html>", None))
    # retranslateUi

