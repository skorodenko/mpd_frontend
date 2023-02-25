import asyncio
import qtinter
import pathlib
from .ui_main import Ui_MainWindow
from .custom_classes.playlists_model import PlaylistsModel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PIL import Image, ImageQt
from io import BytesIO


class InitMainWindow(QMainWindow, Ui_MainWindow):

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

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._binder()

    def _binder(self):
        self.media_previous.clicked.connect(
            qtinter.asyncslot(self._media_previous))
        self.media_play_pause.clicked.connect(
            qtinter.asyncslot(self._media_play_pause))
        self.media_next.clicked.connect(
            qtinter.asyncslot(self._media_next))
        
        self.media_repeat.clicked.connect(
            qtinter.asyncslot(self._media_repeat))
        self.media_shuffle.clicked.connect(
            qtinter.asyncslot(self._media_shuffle))
        
        self.media_seek.sliderMoved.connect(
            qtinter.asyncslot(self._media_seeker))
        
        self.playlists_view.doubleClicked.connect(
            qtinter.asyncslot(self._change_playlist)
        )

    async def __playback_control_init(self, init_status):
        play_state = init_status["state"]
        self.media_previous.setIcon(QIcon.fromTheme("media-skip-backward"))
        await self._icon_media_play_pause(play_state)
        self.media_next.setIcon(QIcon.fromTheme("media-skip-forward"))

    async def __playlist_control_init(self, init_status):
        repeat = init_status["repeat"]
        single = init_status["single"]
        await self._icon_media_repeat(repeat, single)

        shuffle = init_status["random"]
        await self._icon_media_shuffle(shuffle)
    
    async def __media_seek_init(self):
        while True:
            status = await self.mpd_client.status()
            duration = int(float(status.get("duration", 100)))
            elapsed = int(float(status.get("elapsed", 0)))
            
            self.label_time.setText(f"{elapsed//60}:{elapsed%60:0>2}/{duration//60}:{duration%60:0>2}")
            self.media_seek.setMaximum(duration)
            self.media_seek.setSliderPosition(elapsed)

            await asyncio.sleep(0.4)

    async def _change_playlist(self, index):
        await self.ptiling_widget.add_playlist(index.data())

    async def _playlists_view_update(self):
        playlists = await self.mpd_client.listfiles(".")
        self.playlists_model = PlaylistsModel(playlists)
        self.playlists_view.setModel(self.playlists_model)

    async def _init_gui(self, init_status):
        await self.__playback_control_init(init_status)
        await self.__playlist_control_init(init_status)
        await self._playlists_view_update()
        await self._change_cover()
        await self.ptiling_widget._init_connection(self)
        self._media_seek_task = asyncio.create_task(self.__media_seek_init())

    async def _icon_media_play_pause(self, state):
        match state:
            case "play":
                self.media_play_pause.setIcon(QIcon.fromTheme("media-playback-pause"))
            case "stop" | "pause":
                self.media_play_pause.setIcon(QIcon.fromTheme("media-playback-start"))
    
    async def _icon_media_repeat(self, repeat, single):
        match (repeat,single):
            case ("0","0") | ("0","1"): #Second variant is redundant
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-none"))
            case ("1","0"):
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-all"))
            case ("1","1"):
                self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-single"))
    
    async def _icon_media_shuffle(self, shuffle):
        match shuffle:
            case "0":
                self.media_shuffle.setIcon(QIcon.fromTheme("media-playlist-normal"))
            case "1":
                self.media_shuffle.setIcon(QIcon.fromTheme("media-playlist-shuffle"))

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

    async def _change_cover(self, file=None):
        if file:
            if not (art := await self.cache.get(file)):
                art = await self.mpd_client.readpicture(file)
                art = art.get("binary")
                if art:
                    await self.cache.set(file, art)  
            if art:
                art = Image.open(BytesIO(art))
                art.thumbnail((128,128), resample=Image.NEAREST)
                cover = self.expand2square(art, (0,0,0))
                cover = ImageQt.ImageQt(cover)
                cover = QPixmap.fromImage(cover)
            else:
                cover = QIcon.fromTheme("folder-cd") #TODO Add higher res blank cover
                cover = cover.pixmap(cover.actualSize(QSize(128,128))) 
        else:
            cover = QIcon.fromTheme("folder-cd") #TODO Add higher res blank cover
            cover = cover.pixmap(cover.actualSize(QSize(128,128))) 

        self.label_art.setPixmap(cover)