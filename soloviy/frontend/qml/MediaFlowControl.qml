import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami


ColumnLayout {
    id: media_playback_controls
    spacing: 6

    QQC2.Button {
        id: playback_play
        flat: true
        icon.name: "media-repeat-none"
        Layout.preferredWidth: 16
        Layout.preferredHeight: 16
    }

    QQC2.Button {
        id: playback_forward
        flat: true
        icon.name: "media-playlist-normal"
        Layout.preferredWidth: 16
        Layout.preferredHeight: 16
    }
}