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
                id: group_combo
                textRole: "name"
                valueRole: "value"
                onActivated: groups_model.setActive(currentValue)
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                model: groups_model
            }
        }
    }

    UIM.PlaylistsGroup {
        id: groups_model
        onUpdated: function(index) { playlists_model.refresh(index) }
    }

    UIM.Playlists {
        id: playlists_model
    }
    
    Connections {
        target: UIC.Main
        function onConnected() {
            groups_model.refresh()
        }
    }
    
    ListView {
        id: playlists_view
        anchors.fill: parent
        model: playlists_model
        delegate: Item {
            height: 30
            width: playlists_view.width
            
            required property string name
            
            QQC2.Label {
                text: name
                font.pixelSize: 14
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                anchors.verticalCenter: parent.verticalCenter
                elide: Text.ElideRight
            }
        }
    }
}