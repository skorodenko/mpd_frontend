import asyncio
import qtinter
import pathlib
from .ui_main import Ui_MainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class InitMainWindow(QMainWindow, Ui_MainWindow):

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

            await asyncio.sleep(0.6)
    
    async def _init_gui(self, init_status, song):
        await self.__playback_control_init(init_status)
        await self.__playlist_control_init(init_status)
        await self._label_song_change(song)
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

    async def _label_song_change(self, song):
        name = song.get("title", "<title>")
        artist = song.get("artist", "<artist>")
        album = song.get("album", "<album>")
        freq,bitr,_ = song.get("format", "<format>").split(":")
        file = song.get("file", "<file>")
        _, ext = pathlib.Path(file).suffix.split(".")
        self.label_title.setText(name)
        self.label_author.setText(f"{artist} | {album}")
        self.label_info.setText(f"{int(freq)/1000}kHz, {bitr} bit, {ext.upper()}")