import attrs
import grpc
from functools import wraps
from typing import List, Optional
from src.service.api import api_pb2
from src.service.db import state
from src.service.models.pydantic import MetaTile
from src.service.api.api_pb2_grpc import TilingAPIServicer
from src.config import config


@attrs.define
class TilingAPI(TilingAPIServicer):
    tiles: List[MetaTile] = attrs.field(init=False)

    @tiles.default
    def _preload_tiles(self):
        if not state.get("tiles", False):
            state["tiles"] = list()
        return state["tiles"]

    def persist_changes(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            res = fun(self, *args, **kwargs)
            meta_tiles = list(map(lambda t: t.meta, self.tiles))
            state["tiles"] = meta_tiles
            return res

        return wrapper

    @property
    def tmode(self) -> int:
        return config.soloviy.tiling_mode

    @property
    def locked(self) -> int:
        return sum(1 for tile in self.tiles if tile.locked)

    @property
    def first_unlocked(self) -> Optional[int]:
        for i, tile in enumerate(self.tiles):
            if not tile.locked:
                return i

    def AddTile(
        self,
        request: api_pb2.PlaylistName,
        context: grpc.aio.ServicerContext,
    ) -> api_pb2.MetaTile:
        tile = self.add_tile(MetaTile(**request.__dict__))

        return super().AddTile(request, context)

    @persist_changes
    def add_tile(self, tile: MetaTile) -> Optional[MetaTile]:
        if self.locked + 1 > self.tmode:
            return
        if tile in self.tiles:
            return
        if len(self.tiles) + 1 > self.tmode:  # Rotate free tiles
            index = self.first_unlocked
            self.tiles.pop()
            self.tiles.insert(index, tile)
        else:  # Just append tile
            self.tiles.append(tile)
        return tile

    @persist_changes
    def toggle_lock_tile(self, tile: MetaTile):
        if tile.locked:
            tile.locked = False
            self.tiles.sort(key=lambda x: x.locked, reverse=True)
        else:
            tile.locked = True
            self.tiles.sort(key=lambda x: not x.locked)

    @persist_changes
    def remove_tile(self, tile: MetaTile):
        if tile not in self.tiles:
            raise Exception(f"Tile does not exist: {tile.name}")
        self.tiles.remove(tile)

    @persist_changes
    def change_playing_tile(self, tile: MetaTile):
        for _tile in self.tiles:
            if _tile is not tile:
                _tile.playing_pos = None

    @persist_changes
    def change_song(self, pos: Optional[int]):
        for tile in self.tiles:
            if tile.playing_pos is not None:
                if pos is None:
                    tile.playing_pos = pos
                else:
                    tile.playing_pos = int(pos)
        self.sender.meta_updated.emit()

    @persist_changes
    def clear(self):
        self.tiles.clear()
