import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.20 as Kirigami


RowLayout {
    id: media_playback_controls
    spacing: 0

    Controls.Button {
        id: playback_backward
        icon.name: "media-skip-backward"
        flat: true
    }
    Controls.Button {
        id: playback_play
        icon.name: "media-playback-start"
        flat: true
    }
    Controls.Button {
        id: playback_forward
        icon.name: "media-skip-forward"
        flat: true
    }
}