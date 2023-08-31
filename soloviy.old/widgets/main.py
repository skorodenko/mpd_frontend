import attrs
import asyncio
import pathlib
import datetime
from aiocache import Cache, cached
from PIL import Image, ImageQt
from io import BytesIO
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from pyqtconfig import ConfigManager
import soloviy.utils.time_utils as tu
from soloviy.utils.mpd_connector import MpdConnector
from soloviy.models.playlists_model import PlaylistsModel
from soloviy.ui.ui_main import Ui_MainWindow
from soloviy.constants import APP_CONFIG_FILE, APP_DEFAULT_SETTINGS


@attrs.define
class MainWindow(QMainWindow, Ui_MainWindow):
    config: ConfigManager = ConfigManager(APP_DEFAULT_SETTINGS, filename=APP_CONFIG_FILE) 
    cache: Cache = attrs.Factory(Cache)
    timer: QtCore.QTimer = QtCore.QTimer
    mpd: MpdConnector = attrs.Factory(MpdConnector)
    
    def __attrs_pre_init__(self):
        super().__init__()
        QtCore.QDir.addSearchPath("logo", "./soloviy/resources/logo/") 
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        self.media_previous.clicked.connect(self.mpd)
        self.media_play_pause.clicked.connect(MpdConnector.media_play_pause.emit)
        self.media_next.clicked.connect(MpdConnector.media_next.emit)
        
        self.media_repeat.clicked.connect(MpdConnector.media_repeat.emit)
        self.media_shuffle.clicked.connect(MpdConnector.media_shuffle.emit)
        
        self.media_seek.sliderMoved.connect(MpdConnector.media_seeker.emit)
        
        self.playlists_view.doubleClicked.connect(MpdConnector.playlist_change.emit)
    
    def serve(self):
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, MpdConnector.mpd_connect.emit)
    
    @staticmethod
    def expand2square(pil_img, background_color):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    async def __playback_control_init(self, init_status):
        play_state = init_status["state"]
        await self._icon_media_play_pause(play_state)

    async def __playlist_control_init(self, init_status):
        repeat = init_status["repeat"]
        single = init_status["single"]
        await self._icon_media_repeat(repeat, single)

        shuffle = init_status["random"]
        await self._icon_media_shuffle(shuffle)
    
    async def __media_seek_init(self):
        while True:
            status = await self.mpd.client.status()
            duration = int(float(status.get("duration", 100)))
            elapsed = int(float(status.get("elapsed", 0)))
            dd = datetime.timedelta(seconds=duration)
            ed = datetime.timedelta(seconds=elapsed)
            
            self.label_time.setText(f"{tu.strfdelta(ed)}/{tu.strfdelta(dd)}")
            self.media_seek.setMaximum(duration)
            self.media_seek.setSliderPosition(elapsed)

            await asyncio.sleep(0.2)

    async def _change_playlist(self, index):
        await self.ptiling_widget.add_playlist(index.data())

    async def _playlists_view_update(self, playlists):
        self.playlists_model = PlaylistsModel(playlists)
        self.playlists_view.setModel(self.playlists_model)

    async def _init_gui(self, init_status, playlists):
        await self.__playback_control_init(init_status)
        await self.__playlist_control_init(init_status)
        await self._playlists_view_update(playlists)
        await self._change_cover()
        self.ptiling_widget._init_connection(self)
        self._media_seek_task = asyncio.create_task(self.__media_seek_init())

    async def _icon_media_play_pause(self, state):
        match state:
            case "play":
                self.media_play_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-pause"))
            case "stop" | "pause":
                self.media_play_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-start"))
    
    async def _icon_media_repeat(self, repeat, single):
        match (repeat,single):
            case ("0","0") | ("0","1"): #Second variant is redundant
                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-none"))
            case ("1","0"):
                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-all"))
            case ("1","1"):
                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-single"))
    
    async def _icon_media_shuffle(self, shuffle):
        match shuffle:
            case "0":
                self.media_shuffle.setIcon(QtGui.QIcon.fromTheme("media-playlist-normal"))
            case "1":
                self.media_shuffle.setIcon(QtGui.QIcon.fromTheme("media-playlist-shuffle"))

    async def _label_song_change(self, df):
        name = df["title"]
        artist = df["artist"]
        album = df["album"]
        freq = df["freq"]
        bitr = df["bitr"]
        file = df["file"]
        _, ext = pathlib.Path(file).suffix.split(".")
        
        light_font = QApplication.font()
        light_font.setWeight(light_font.weight()//2)
        light_font.setPointSize(light_font.pointSize() - 1)

        self.label_time.setFont(light_font)
        self.label_title.setText(name)
        self.label_author.setText(f"{artist} | {album}")
        self.label_author.setFont(light_font)
        self.label_info.setText(f"{int(freq)/1000}kHz, {bitr} bit, {ext}")
        self.label_info.setFont(light_font)

        await self._change_cover(file)

    @cached()
    async def _get_cover(self, file):
        if not file:
            return None
        art = await self.mpd.client.readpicture(file)
        art = art.get("binary")
        return art

    async def _change_cover(self, file=None):
        art = await self._get_cover(file)
        
        if art:
            art = Image.open(BytesIO(art))
            art.thumbnail((128,128), resample=Image.LANCZOS)
            cover = self.expand2square(art, (0,0,0))
            cover = ImageQt.ImageQt(cover)
            cover = QtGui.QPixmap.fromImage(cover)
        else:
            cover = QtGui.QIcon.fromTheme("folder-cd") #TODO Add higher res blank cover
            cover = cover.pixmap(cover.actualSize(QtCore.QSize(128,128))) 

        self.label_art.setPixmap(cover)


    def closeEvent(self, event):
        if self.mpd_idle_task:
            self.mpd_idle_task.cancel()
        self.mpd.mpd_disconnect(self.config.get("mpd_socket"))
        super().closeEvent(event)
    