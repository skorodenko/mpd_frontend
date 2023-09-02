import attrs
import logging
import asyncio
import pathlib
import datetime
from dynaconf.loaders.toml_loader import write
import qtinter
from PIL import Image, ImageQt
from io import BytesIO
from PySide6.QtCore import QDir, QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from soloviy.config import settings
from soloviy.models.playlists import PlaylistsModel
#import soloviy.utils.time_utils as tu
from soloviy.api.mpd_connector import MpdConnector
#from soloviy.models.playlists_model import PlaylistsModel
from soloviy.ui.ui_main_window import Ui_MainWindow
from soloviy.widgets.init_wizard import InitWizard


logger = logging.getLogger(__name__)


class SingalsMixin(QObject):
    ...


@attrs.define
class MainWindow(QMainWindow, Ui_MainWindow, SingalsMixin):
    timer: QTimer = QTimer
    mpd: MpdConnector = attrs.Factory(MpdConnector)
    init_wizard: InitWizard = attrs.Factory(InitWizard, takes_self=True)
    
    def __attrs_pre_init__(self):
        super().__init__()
        QDir.addSearchPath("icons", "./soloviy/ui/icons/") 
        self.setupUi(self)
    
    def __attrs_post_init__(self):
        self._bind_signals()
        
    def serve(self):
        logger.info("Started main window")
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(100, self._initial_configuration)
 
    def _initial_configuration(self):
        logger.info("Started initial configuration")
        if not settings.mpd.socket:
            if self.init_wizard.exec() == QDialog.DialogCode.Rejected:
                self.close()
            else:
                self.persist_settings()
        else:
            self.init_wizard.connect_mpd.emit(settings.mpd.socket)
                
    def _bind_signals(self):
        self.mpd.mpd_connection_status.connect(
            qtinter.asyncslot(self.init_wizard.connect_mpd_tracker)
        )
        self.mpd.update_playlists_view.connect(
            self.__update_playlists_view
        )
        self.init_wizard.connect_mpd.connect(
            qtinter.asyncslot(self.mpd.mpd_connect)
        )
    
    def __update_playlists_view(self, playlists: list):
        playlists_model = PlaylistsModel(playlists)
        self.playlists_view.setModel(playlists_model)
    
    @staticmethod
    def persist_settings(): #TODO move to settings widget
        logger.info("Persisted settings")
        data = settings.as_dict()
        write(settings.settings_file, data)
        
    def closeEvent(self, event):
        logger.info("Closing main window")
        self.mpd.graceful_close()
        super().closeEvent(event)
    
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
#    async def __playback_control_init(self, init_status):
#        play_state = init_status["state"]
#        await self._icon_media_play_pause(play_state)
#
#    async def __playlist_control_init(self, init_status):
#        repeat = init_status["repeat"]
#        single = init_status["single"]
#        await self._icon_media_repeat(repeat, single)
#
#        shuffle = init_status["random"]
#        await self._icon_media_shuffle(shuffle)
#    
#    async def __media_seek_init(self):
#        while True:
#            status = await self.mpd.client.status()
#            duration = int(float(status.get("duration", 100)))
#            elapsed = int(float(status.get("elapsed", 0)))
#            dd = datetime.timedelta(seconds=duration)
#            ed = datetime.timedelta(seconds=elapsed)
#            
#            self.label_time.setText(f"{tu.strfdelta(ed)}/{tu.strfdelta(dd)}")
#            self.media_seek.setMaximum(duration)
#            self.media_seek.setSliderPosition(elapsed)
#
#            await asyncio.sleep(0.2)
#
#    async def _change_playlist(self, index):
#        await self.ptiling_widget.add_playlist(index.data())
#
#    async def _playlists_view_update(self, playlists):
#        self.playlists_model = PlaylistsModel(playlists)
#        self.playlists_view.setModel(self.playlists_model)
#
#    async def _init_gui(self, init_status, playlists):
#        await self.__playback_control_init(init_status)
#        await self.__playlist_control_init(init_status)
#        await self._playlists_view_update(playlists)
#        await self._change_cover()
#        self.ptiling_widget._init_connection(self)
#        self._media_seek_task = asyncio.create_task(self.__media_seek_init())
#
#    async def _icon_media_play_pause(self, state):
#        match state:
#            case "play":
#                self.media_play_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-pause"))
#            case "stop" | "pause":
#                self.media_play_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-start"))
#    
#    async def _icon_media_repeat(self, repeat, single):
#        match (repeat,single):
#            case ("0","0") | ("0","1"): #Second variant is redundant
#                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-none"))
#            case ("1","0"):
#                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-all"))
#            case ("1","1"):
#                self.media_repeat.setIcon(QtGui.QIcon.fromTheme("media-repeat-single"))
#    
#    async def _icon_media_shuffle(self, shuffle):
#        match shuffle:
#            case "0":
#                self.media_shuffle.setIcon(QtGui.QIcon.fromTheme("media-playlist-normal"))
#            case "1":
#                self.media_shuffle.setIcon(QtGui.QIcon.fromTheme("media-playlist-shuffle"))
#
#    async def _label_song_change(self, df):
#        name = df["title"]
#        artist = df["artist"]
#        album = df["album"]
#        freq = df["freq"]
#        bitr = df["bitr"]
#        file = df["file"]
#        _, ext = pathlib.Path(file).suffix.split(".")
#        
#        light_font = QApplication.font()
#        light_font.setWeight(light_font.weight()//2)
#        light_font.setPointSize(light_font.pointSize() - 1)
#
#        self.label_time.setFont(light_font)
#        self.label_title.setText(name)
#        self.label_author.setText(f"{artist} | {album}")
#        self.label_author.setFont(light_font)
#        self.label_info.setText(f"{int(freq)/1000}kHz, {bitr} bit, {ext}")
#        self.label_info.setFont(light_font)
#
#        await self._change_cover(file)
#
#    @cached()
#    async def _get_cover(self, file):
#        if not file:
#            return None
#        art = await self.mpd.client.readpicture(file)
#        art = art.get("binary")
#        return art
#
#    async def _change_cover(self, file=None):
#        art = await self._get_cover(file)
#        
#        if art:
#            art = Image.open(BytesIO(art))
#            art.thumbnail((128,128), resample=Image.LANCZOS)
#            cover = self.expand2square(art, (0,0,0))
#            cover = ImageQt.ImageQt(cover)
#            cover = QtGui.QPixmap.fromImage(cover)
#        else:
#            cover = QtGui.QIcon.fromTheme("folder-cd") #TODO Add higher res blank cover
#            cover = cover.pixmap(cover.actualSize(QtCore.QSize(128,128))) 
#
#        self.label_art.setPixmap(cover)
