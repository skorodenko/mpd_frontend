import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami
import main 1.0 as Main
import controllers 1.0 as UIC


Kirigami.ApplicationWindow {
    id: root
    title: qsTr("Soloviy")
    pageStack.initialPage: [playlists, player]
    
    Component.onCompleted: UIC.Main.connect()
    
    Main.PagePlaylists {
        id: playlists
    }

    Main.PagePlayer {
        id: player
    }
}
