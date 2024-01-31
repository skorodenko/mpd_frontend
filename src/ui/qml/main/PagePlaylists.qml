import QtQml 2.15
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami
import controllers 1.0 as UIC
import models 1.0 as UIM


Kirigami.ScrollablePage {
    id: root
    globalToolBarStyle: Kirigami.ApplicationHeaderStyle.None
    
    header: QQC2.ToolBar {
        implicitHeight: 48
        RowLayout {
            anchors.fill: parent

            Kirigami.Heading {
                text: "Group by:"
            }

            QQC2.ComboBox {
                id: searchField
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                model: ListModel {
                    id: model
                    ListElement { text: "Banana" }
                    ListElement { text: "Apple" }
                    ListElement { text: "Coconut" }
                }
            }
        }
    }

    UIM.PlaylistsModel {
        id: playlists_model
    }
    
    Connections {
        target: UIC.Main
        function onConnected() {
            playlists_model.update_playlists()
        }
    }
    
    ListView {
        id: playlists_view
        anchors.fill: parent
        model: playlists_model
        delegate: Text {
                required property string name
                text: name
            }
    }
}