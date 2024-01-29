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

            RowLayout {
                id: media_playback_controls
                spacing: 0

                QQC2.Button {
                    id: playback_backward
                    icon.name: "media-skip-backward"
                    flat: true
                }
                QQC2.Button {
                    id: playback_play
                    icon.name: "media-playback-start"
                    flat: true
                }
                QQC2.Button {
                    id: playback_forward
                    icon.name: "media-skip-forward"
                    flat: true
                }
            }

            ColumnLayout {
                spacing: 0

                RowLayout {
                    QQC2.Label {
                        id: media_title
                        text: "Title | Author"
                        Layout.fillWidth: true
                    }
                    QQC2.Label {
                        id: media_duration
                        text: "0:00 / 0:00"
                        Layout.rightMargin: Qt.Infinity
                    }
                }

                RowLayout {
                    QQC2.Slider {
                        id: media_seeker
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}