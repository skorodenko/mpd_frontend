from PySide6.QtCore import Qt, QAbstractTableModel, QAbstractListModel


VISIBLE_COLUMNS = ["track", "file"]  # Move to config


class PlaylistModel(QAbstractTableModel):
    ...


class PlaylistsModel(QAbstractListModel):
    ...