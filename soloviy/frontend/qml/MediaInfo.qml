import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15 as QQC2
import org.kde.kirigami 2.20 as Kirigami


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
