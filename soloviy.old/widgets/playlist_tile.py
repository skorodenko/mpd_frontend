import asyncio
import qtinter
import pandas as pd
from PyQt6 import QtWidgets
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models.playlist_model import PlaylistModel


class PlaylistTile(QtWidgets.QFrame, Ui_Frame):
    def __init__(self, tiler, playlist):
        super().__init__()
        self.setupUi(self)
        self.tiler = tiler
        self.lock_status = False
        #TODO Global config here
        hidden = ["__playing", "file", "last-modified", "genre", 
                  "date", "freq", "bitr", "chanels", "disc",
                  "album", "composer"]
        match playlist:
            case [{"directory": title}, *etc]:
                self.title = title
                playlist = [d for d in etc if d.get("file") is not None]
                self.playlist = pd.DataFrame.from_dict(playlist)
                self.playlist = self.playlist.assign(__playing=False)
                self.playlist[["freq","bitr","chanels"]] = self.playlist["format"].str.split(":", expand=True)
                self.playlist.insert(0, "#", self.playlist["track"])
                self.playlist.drop("track", inplace=True, axis=1)
                self.playlist = self.playlist.reindex(
                    columns = [c for c in self.playlist.columns if c != "time"] + ["time"]
                )
                self.playlist.drop("format", inplace=True, axis=1)
                self.playlist.drop("duration", inplace=True, axis=1)
                self.playlist["last-modified"] = pd.to_datetime(self.playlist["last-modified"])
                self.playlist = self.playlist.astype({
                    "#":"int",
                    "time":"int",
                }, errors="ignore")
                self.playlist["time"] = pd.to_timedelta(self.playlist["time"], unit="S")
        self.playlist_title.setText(self.title)
        self.playlist_model = PlaylistModel(self.playlist)
        self.playlist_table.setModel(self.playlist_model)

        self._hidden = {k:False for k in self.playlist.columns}
        self._hidden.update({k:True for k in hidden if k in self.playlist.columns})
        self.hide_columns()

        self._init_resize()
        
        self.playlist_table.horizontalHeader().sortIndicatorChanged.connect(
            qtinter.asyncslot(self.header_sort)
        )
        self.playlist_table.doubleClicked.connect(
            qtinter.asyncslot(self.play_song)
        )
        self.playlist_lock.clicked.connect(
            qtinter.asyncslot(self.lock)
        )
        self.playlist_destroy.clicked.connect(
            qtinter.asyncslot(self.destroy)
        )
    
    def _init_resize(self):
        head = self.playlist_table.horizontalHeader()
        visible_count = head.count() - head.hiddenSectionCount()
        for vi in range(0, visible_count):
            head.setSectionResizeMode(head.logicalIndex(vi), QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def hide_columns(self):
        for c in self._hidden:
            self.playlist_table.setColumnHidden(
                self.playlist.columns.to_list().index(c),
                self._hidden[c]
            )

    async def header_sort(self, section, order):
        self.playlist_model.sort(section, bool(order))
        if self.tiler.active_playlist == self:
            kv = {k:v for k,v in zip(
                range(len(self.playlist)),
                self.playlist.index.to_list())}
            await asyncio.create_task(self.tiler.sort_playlist(kv))
        self.playlist_model.reset_index()

    async def play_song(self, index):
        tile = self
        playlist = self.playlist_model.playlist
        song_pos = index.row()
        await self.tiler.playlist_song(tile, playlist, song_pos)

    async def lock(self, status):
        self.lock_status = status
        await self.tiler.playlist_lock(self, status)

    async def destroy(self):
        await self.tiler.playlist_destroy(self)