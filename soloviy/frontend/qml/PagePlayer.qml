import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami


Kirigami.Page {
    id: root
    globalToolBarStyle: Kirigami.ApplicationHeaderStyle.None
    
    header: QQC2.ToolBar {
        implicitHeight: 48
        RowLayout {
            spacing: 8
            anchors.rightMargin: 8
            anchors.fill: parent

            MediaPlaybackControl {}

            ColumnLayout {
                spacing: 0

                MediaInfo {}

                MediaSeeker {}
            }
            
            MediaFlowControl {}
        }
    }
}