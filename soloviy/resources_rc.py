# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.6.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x01V\
i\
mport QtQuick 2.\
15\x0aimport QtQuic\
k.Layouts 1.15\x0ai\
mport QtQuick.Co\
ntrols 2.15 as Q\
QC2\x0aimport org.k\
de.kirigami 2.20\
 as Kirigami\x0a\x0a\x0aK\
irigami.Applicat\
ionWindow {\x0a    \
id: root\x0a    tit\
le: qsTr(\x22Solovi\
y\x22)\x0a    pageStac\
k.initialPage: [\
playlists, playe\
r]\x0a    \x0a    Page\
Playlists {\x0a    \
    id: playlist\
s\x0a    }\x0a\x0a    Pag\
ePlayer {\x0a      \
  id: player\x0a   \
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
\x00\x00\x01\x8c\xda\x8c\xdf\x0d\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
