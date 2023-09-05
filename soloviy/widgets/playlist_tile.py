import attrs
import asyncio
import qtinter
import tinydb
from PySide6.QtWidgets import QFrame, QHeaderView
from soloviy.ui.ui_playlist_tile import Ui_Frame
from soloviy.models.playlist_qmodel import PlaylistModel


@attrs.define
class PlaylistTile(QFrame, Ui_Frame):
    playlist: str
    lock_status: bool = False 
    
    def __attrs_pre_init__(self):
        super().__init__()
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        pmodel = PlaylistModel(self.playlist)
        self.playlist_table.setModel(pmodel)
