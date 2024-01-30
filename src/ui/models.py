# from soloviy.backend.db import state
from PySide6.QtCore import Qt, QAbstractTableModel, QAbstractListModel
# from soloviy.models.dbmodels import Library
# from soloviy.api.tiling import QMetaTile

VISIBLE_COLUMNS = ["track", "file"]  # Move to config


class PlaylistModel(QAbstractTableModel):
    ...


class PlaylistsModel(QAbstractListModel):
    def __init__(self):
        self.update_playlists()

    def update_playlists(self):
        self.layoutAboutToBeChanged.emit()

        self.layoutChanged.emit()


# class PlaylistModel(QAbstractTableModel):
#    def __init__(self, qmeta: QMetaTile):
#        super().__init__()
#        self.qmeta: QMetaTile = qmeta
#        self.columns: list[str] = VISIBLE_COLUMNS
#        self.group_by: str = state["group_by"]
#        self._query = Library.select().where(getattr(Library, self.group_by) == self.qmeta.name)
#        self.sort(
#            self.columns.index(qmeta.order_by[0]),
#            qmeta.order_by[1]
#        )
#
#    @property
#    def query(self):
#        return self._query
#
#    @staticmethod
#    def strfdelta(tdelta):
#        h, rem = divmod(tdelta, 3600)
#        m, s = divmod(rem, 60)
#        match h,m,s:
#            case h,_,_ if h != 0:
#                return f"{h}:{m:0>2}:{s:0>2}"
#            case _:
#                return f"{m:0>2}:{s:0>2}"
#
#    def data(self, index, role):
#        row = index.row()
#        column = index.column()
#        if role == Qt.ItemDataRole.DisplayRole:
#            column_name = self.columns[column]
#            val = getattr(self.query[row], column_name)
#            if column_name == "time":
#                return self.strfdelta(val)
#            return str(val)
#        if role == Qt.ItemDataRole.DecorationRole:
#            if column == 0 and row == self.qmeta.playing_pos:
#                return PLAYING_ICON
#
#    def rowCount(self, index):
#        return self._query.count()
#
#    def columnCount(self, index):
#        return len(self.columns)
#
#    def headerData(self, section, orientation, role):
#        if role == Qt.ItemDataRole.DisplayRole:
#            if orientation == Qt.Orientation.Horizontal:
#                if section == self.columns.index("track"):
#                    return "#"
#                return self.columns[section]
#
#    def sort(self, section, order):
#        # Updated meta tile object
#        col_str = self.columns[section]
#        self.qmeta.order_by = (col_str, order)
#
#        # Update ui with new query
#        self.layoutAboutToBeChanged.emit()
#        col = getattr(Library, col_str)
#        if order is Qt.SortOrder.DescendingOrder:
#            self._query = self._query.order_by(-col)
#        else:
#            self._query = self._query.order_by(col)
#        self.layoutChanged.emit()
#
#
# class PlaylistsModel(QAbstractListModel):
#    def __init__(self, playlists):
#        super().__init__()
#        self.playlists = playlists
#
#    def data(self, index, role):
#        if role == Qt.ItemDataRole.DisplayRole:
#            name = self.playlists[index.row()]
#            return name
#        if role == Qt.ItemDataRole.DecorationRole:
#            return FOLDER_ICON
#
#    def rowCount(self, index):
#        return len(self.playlists)
