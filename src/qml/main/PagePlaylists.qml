import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami


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

    QQC2.Label {
        // Center label horizontally and vertically within parent object
        anchors.centerIn: parent
        text: qsTr("Hello World!")
    }

}