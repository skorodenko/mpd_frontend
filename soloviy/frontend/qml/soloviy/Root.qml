import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami
import soloviy 1.0


Kirigami.ApplicationWindow {
    id: root
    title: qsTr("Soloviy")
    pageStack.initialPage: [playlists, player]
    
    PagePlaylists {
        id: playlists
    }

    PagePlayer {
        id: player
    }
}
