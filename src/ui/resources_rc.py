# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.6.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x01i\
i\
mport QtQuick 2.\
15\x0aimport QtQuic\
k.Layouts 1.15\x0ai\
mport QtQuick.Co\
ntrols 2.15 as Q\
QC2\x0aimport org.k\
de.kirigami 2.20\
 as Kirigami\x0aimp\
ort soloviy 1.0\x0a\
\x0a\x0aKirigami.Appli\
cationWindow {\x0a \
   id: root\x0a    \
title: qsTr(\x22Sol\
oviy\x22)\x0a    pageS\
tack.initialPage\
: [playlists, pl\
ayer]\x0a    \x0a    P\
agePlaylists {\x0a \
       id: playl\
ists\x0a    }\x0a\x0a    \
PagePlayer {\x0a   \
     id: player\x0a\
    }\x0a}\x0a\
"

qt_resource_name = b"\
\x00\x08\
\x06g_\x1c\
\x00R\
\x00o\x00o\x00t\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8dY\x00U9\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
