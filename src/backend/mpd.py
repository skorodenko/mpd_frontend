import socket
import attrs
import grpc
import asyncio
import logging
from subprocess import Popen
from PIL import Image, ImageQt
from io import BytesIO
from src.backend.db import state
from enum import Enum, auto
from typing import List
from pydantic import TypeAdapter
from mpd.asyncio import MPDClient

# from soloviy.backend.api import library
from src.config import settings
from src.backend.models.db import Library
from src.backend.models import pydantic as pmodels
from src.backend.api import api_pb2_grpc, api_pb2


logger = logging.getLogger(__name__)


class MPDAction(Enum):
    SORT = auto()
    SONG_CHANGE = auto()


class ConnectionStatus(Enum):
    """Connection status update"""

    CONNECTED = auto()
    CONNECTING = auto()
    DISCONNECTED = auto()
    CONNECTION_LOST = auto()
    CONNECTION_TIMEOUT = auto()
    CONNECTION_FAILED = auto()


@attrs.define
class MpdService(api_pb2_grpc.MpdAPIServicer):
    mpd_server: Popen = None
    idle: asyncio.Task = None
    client: MPDClient = attrs.Factory(MPDClient)
    mpd_binary: bool = attrs.field(init=False)

    @mpd_binary.default
    def _factory_mpd_binary(self) -> bool:
        from shutil import which

        return which("mpd") is not None

    def __attrs_pre_init__(self):
        super().__init__()

    async def mpd_connect(self, _socket: str):
        logger.info("Connecting to mpd")
        if _socket == settings.mpd.native_socket:
            if not self.mpd_binary:
                logger.error("Can't find mpd binary in PATH")
            logger.info("Starting native mpd server")
            self.mpd_server = Popen(["mpd", settings.mpd.native_config, "--no-daemon"])
            await asyncio.sleep(0.5)
        try:
            logging.debug(f"Socket: {_socket}")
            await self.client.connect(_socket)
            logger.info("Successfuly connected to mpd")
        except (socket.gaierror, ConnectionRefusedError):
            logger.warning("Failed to connect to mpd")

    #    @staticmethod
    #    def group_by_folders(data: list[dict]) -> dict[list[dict]]:
    #        res = dict()
    #        for item in data:
    #            if directory := item.get("directory"):
    #                res[directory] = []
    #                partial_res = res[directory]
    #                continue
    #            partial_res.append(item)
    #        return res
    #
    #    async def _handle_tile_gateway(self, tile: MetaTile, action: MPDAction):
    #        match action, state.get("prev_tile"):
    #            case MPDAction.SONG_CHANGE, None:
    #                await self._populate_playlist(tile)
    #                await self.client.play(tile.playing_pos)
    #
    #            case MPDAction.SORT, None:
    #                pass
    #
    #            case MPDAction.SONG_CHANGE, _ as prev_tile:
    #                if tile.name != prev_tile.name:
    #                    await self.client.clear()
    #                    await self._populate_playlist(tile)
    #                await self.client.play(tile.playing_pos)
    #
    #            case (MPDAction.SORT, _ as prev_tile) if tile.name == prev_tile.name:
    #                await self._sort_playlist(prev_tile, tile)
    #
    #        state["prev_tile"] = tile
    #
    #    async def _populate_playlist(self, tile: MetaTile) -> int:
    #        playlist = library.get_playlist(tile)
    #        for i, song in enumerate(playlist):
    #            await self.client.addid(song.file, i)
    #        return len(playlist)
    #
    #    async def _sort_playlist(self, old_tile: MetaTile, new_tile: MetaTile):
    #        np = library.get_playlist(new_tile)
    #        op = list(library.get_playlist(old_tile))
    #        for _to, song in enumerate(np):
    #            _from = op.index(song)
    #            await self.client.move(_from, _to)
    #
    #    async def update_db(self):
    #        logger.debug("Started db update")
    #        await self.client.update()
    #        data = await self.client.listallinfo()
    #        data = self.group_by_folders(data)
    #        for directory in data:
    #            ta = TypeAdapter(List[pmodels.Library])
    #            sdata = data[directory]
    #            sdata = [i for i in sdata if i.get("file")]
    #            sdata = ta.validate_python(sdata, context={"directory": directory})
    #            sdata = ta.dump_python(sdata)
    #            Library.insert_many(sdata).execute()
    #        logger.debug("Ended db update")
    #        self.db_updated.emit()
    #
    #    def manage_seeker_update_task(self, field: str, status: dict):
    #        if field == "state":
    #            match status["state"], self.seeker_update:
    #                case "play", None:
    #                    self.seeker_update = asyncio.create_task(
    #                        self.seeker_update_task()
    #                    )
    #                case "pause" | "stop", task if task:
    #                    self.seeker_update.cancel()
    #                    self.seeker_update = None
    #
    #    async def seeker_update_task(self):
    #        while True:
    #            status = await self.client.status()
    #            elapsed = int(float(status.get("elapsed", 0)))
    #            duration = int(float(status.get("duration", 100)))
    #            self.update_seeker.emit(duration, elapsed)
    #            await asyncio.sleep(0.2)
    #
    #    def manage_idle_task(self, status: ConnectionStatus):
    #        match status, self.idle:
    #            case ConnectionStatus.CONNECTED, None:
    #                self.idle = asyncio.create_task(self.idle_task())
    #            case _:
    #                return
    #
    #    @staticmethod
    #    def expand2square(pil_img, background_color):
    #        width, height = pil_img.size
    #        if width == height:
    #            return pil_img
    #        elif width > height:
    #            result = Image.new(pil_img.mode, (width, width), background_color)
    #            result.paste(pil_img, (0, (width - height) // 2))
    #            return result
    #        else:
    #            result = Image.new(pil_img.mode, (height, height), background_color)
    #            result.paste(pil_img, ((height - width) // 2, 0))
    #            return result
    #
    #    #TODO Add async cache[disk]
    #    async def _get_cover(self, uri: str) -> QPixmap:
    #        match uri:
    #            case None:
    #                cover = QIcon.fromTheme("folder-cd")
    #                cover = cover.pixmap(cover.actualSize(QSize(128,128)))
    #            case _:
    #                art = await self.client.readpicture(uri)
    #                art = art.get("binary")
    #
    #                if art:
    #                    art = Image.open(BytesIO(art))
    #                    art.thumbnail((128,128), resample=Image.LANCZOS)
    #                    cover = self.expand2square(art, (0,0,0))
    #                    cover = ImageQt.ImageQt(cover)
    #                    cover = QPixmap.fromImage(cover)
    #                else:
    #                    cover = QIcon.fromTheme("folder-cd")
    #                    cover = cover.pixmap(cover.actualSize(QSize(128,128)))
    #        return cover
    #
    #    async def _update_song_info(self, field: str, status: dict):
    #        if field in ["songid", "playlist"]:
    #            info = await self.client.currentsong()
    #            cover = await self._get_cover(info.get("file"))
    #            self.song_changed.emit(info, cover)
    #
    #    @staticmethod
    #    def status_diff(old, new):
    #        return [
    #            k for k in old.keys()
    #            if old.get(k) != new.get(k)
    #            and old.get(k) is not None
    #            and new.get(k) is not None
    #        ]
    #
    #    async def idle_task(self):
    #        logger.debug("Staring idle task")
    #        idle_init = await self.client.status()
    #        state["idle"] = idle_init
    #
    #        logger.debug("Staring ui init")
    #        # Init ui with coresponding init status
    #        for d in idle_init:
    #            self.mpd_idle_update.emit(d, idle_init)
    #        logger.debug("Ended ui init")
    #
    #        logger.debug("Started idle task")
    #        async for subsystem in self.client.idle():
    #            if subsystem:
    #                new = await self.client.status()
    #                old = state["idle"]
    #                diff = self.status_diff(old, new)
    #                for d in diff:
    #                    self.mpd_idle_update.emit(d, new)
    #                state["idle"] = new
    #
    #    async def media_previous(self):
    #        await self.client.previous()
    #
    #    async def media_next(self):
    #        await self.client.next()
    #
    #    async def media_seeker(self, value):
    #        await self.client.seekcur(value)
    #
    #    async def media_play_pause(self):
    #        status = await self.client.status()
    #        match status["state"]:
    #            case "stop":
    #                await self.client.play(status["song"])
    #            case "pause":
    #                await self.client.pause(0)
    #            case "play":
    #                await self.client.pause(1)
    #
    #    async def media_repeat(self):
    #        status = await self.client.status()
    #        repeat = status["repeat"]
    #        single = status["single"]
    #        match (repeat,single):
    #            case ("0","0") | ("0","1"):
    #                await self.client.repeat(1)
    #                await self.client.single(0)
    #            case ("1","0"):
    #                await self.client.repeat(1)
    #                await self.client.single(1)
    #            case ("1","1"):
    #                await self.client.repeat(0)
    #                await self.client.single(0)
    #
    #    async def media_shuffle(self):
    #        status = await self.client.status()
    #        shuffle = status["random"]
    #        match shuffle:
    #            case "0":
    #                await self.client.random(1)
    #            case "1":
    #                await self.client.random(0)

    def graceful_close(self):
        # if self.idle:
        #    self.idle.cancel()
        if self.client and self.client.connected:
            self.client.disconnect()
        if settings.mpd.socket == settings.mpd.native_socket:
            self.mpd_server.wait(2)
