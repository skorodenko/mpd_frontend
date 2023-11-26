import logging
from soloviy.db import state
from soloviy.api.tiling import MetaTile
from soloviy.models.dbmodels import Library
from PySide6.QtCore import Qt


logger = logging.getLogger(__name__)


def get_playlist(tile: MetaTile):
    query = (
        Library
            .select()
            .where(
                getattr(Library, state["group_by"]) == tile.name
            )
    )
    return sort_playlist(tile, query)

def sort_playlist(tile: MetaTile, playlist):
    col = getattr(Library, tile.order_by[0])
    if tile.order_by[1] is Qt.SortOrder.DescendingOrder:
        playlist = playlist.order_by(-col)
    else:
        playlist = playlist.order_by(col)
    return playlist

def get_song(tile: MetaTile):
    #IMPORTANT
    playlist = get_playlist(tile)
    song = playlist[tile.playing_pos]
    return song
