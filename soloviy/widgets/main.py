import sys
import qtinter
import attr
import asyncio
import pathlib
import datetime
from aiocache import Cache
from PIL import Image, ImageQt
from io import BytesIO
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtconfig import ConfigManager
from .playlists_model import PlaylistsModel
import soloviy.utils.time_utils as tu
from soloviy.utils.mpd_connector import MpdConnector
from soloviy.ui.ui_main import Ui_MainWindow
from soloviy.constants import APP_CONFIG_FILE, APP_DEFAULT_SETTINGS


@attr.define
class MainWindow(QMainWindow, Ui_MainWindow):
    config: ConfigManager = ConfigManager(APP_DEFAULT_SETTINGS, filename=APP_CONFIG_FILE) 
    cache: Cache = attr.Factory(Cache)
    timer: QtCore.QTimer = QtCore.QTimer
    mpd: MpdConnector = attr.field()
 
    def __init__(self):
        super().__init__()
        self.__attrs_init__()
    
    @mpd.default
    def _mpd_factory(self):
        obj = MpdConnector()
        obj.attach_to_main(self)
        return obj

    @staticmethod
    def status_diff(old, new):
        return [k for k in old.keys() 
            if old.get(k) != new.get(k)
            and old.get(k) is not None
            and new.get(k) is not None]
        
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
        self.media_previous.setIcon(QtGui.QIcon.fromTheme("media-skip-backward"))
        await self._icon_media_play_pause(play_state)
        self.media_next.setIcon(QtGui.QIcon.fromTheme("media-skip-forward"))

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

            await asyncio.sleep(0.4)

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

        if file != "Unknown.Unknown":        
            await self._change_cover(file)
        else:
            await self._change_cover()

    async def _change_cover(self, file=None):
        art = await self.cache.get(file)
        
        if art:
            art = art["binary"]
            art = Image.open(BytesIO(art))
            art.thumbnail((128,128), resample=Image.LANCZOS)
            cover = self.expand2square(art, (0,0,0))
            cover = ImageQt.ImageQt(cover)
            cover = QtGui.QPixmap.fromImage(cover)
        else:
            cover = QtGui.QIcon.fromTheme("folder-cd") #TODO Add higher res blank cover
            cover = cover.pixmap(cover.actualSize(QtCore.QSize(128,128))) 

        self.label_art.setPixmap(cover)

    def serve(self):
        self.setupUi(self)
        QtCore.QDir.addSearchPath("logo", "./soloviy/resources/logo/") 

        self.__bind_to_widget()
        
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, qtinter.asyncslot(self.mpd.mpd_connect_dialog))
    
    def __bind_to_widget(self):
        self.media_previous.clicked.connect(
            qtinter.asyncslot(self.mpd._media_previous))
        self.media_play_pause.clicked.connect(
            qtinter.asyncslot(self.mpd._media_play_pause))
        self.media_next.clicked.connect(
            qtinter.asyncslot(self.mpd._media_next))
        
        self.media_repeat.clicked.connect(
            qtinter.asyncslot(self.mpd._media_repeat))
        self.media_shuffle.clicked.connect(
            qtinter.asyncslot(self.mpd._media_shuffle))
        
        self.media_seek.sliderMoved.connect(
            qtinter.asyncslot(self.mpd._media_seeker))
        
        self.playlists_view.doubleClicked.connect(
            qtinter.asyncslot(self._change_playlist))

    async def _mpd_idle(self):
        #FIXME Find a way to cancel this task properly
        #FIXME Restart on disconnect
        self.mpd.client.update()
        idle_cache = await self.mpd.client.status()
        playlists = await self.mpd.client.listfiles(".")
        await self.cache.set("idle", idle_cache)
        await self._init_gui(idle_cache, playlists)
        async for subsys in self.mpd.client.idle():
            if subsys:
                new = await self.mpd.client.status()
                idle_cache = await self.cache.get("idle")
                diff = self.status_diff(idle_cache, new)
                await self._route_async_changes(diff, new)
                await self.cache.set("idle", new)


    async def _route_async_changes(self, diff, status):
        for d in diff:
            match d:
                case "state":
                    state = status["state"]
                    await self._icon_media_play_pause(state)
                case "repeat" | "single":
                    repeat = status["repeat"]
                    single = status["single"]
                    await self._icon_media_repeat(repeat, single)
                case "random":
                    shuffle = status["random"]
                    await self._icon_media_shuffle(shuffle)
                case "song" | "playlist":
                    await self.ptiling_widget.song_changed()

    def closeEvent(self, event):
        self.mpd._mpd_disconnect(self.config.get("mpd_socket"))
        super().closeEvent(event)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with qtinter.using_asyncio_from_qt():
        main_window = MainWindow()
        main_window.serve()
        app.exec()