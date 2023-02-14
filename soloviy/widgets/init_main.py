import asyncio
from .ui_main import Ui_MainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow


class InitMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    async def __playback_control_init(self, init_status):
        play_state = init_status["state"]
        self.media_previous.setIcon(QIcon.fromTheme("media-skip-backward"))
        await self._icon_media_play_pause(play_state)
        self.media_next.setIcon(QIcon.fromTheme("media-skip-forward"))

        self.media_previous.clicked.connect(self._media_previous)
        self.media_play_pause.clicked.connect(self._media_play_pause)
        self.media_next.clicked.connect(self._media_next)

    async def __playlist_control_init(self, init_status):
        repeat = init_status["repeat"]
        single = init_status["single"]
        await self._icon_media_repeat(repeat, single)
        self.media_repeat.clicked.connect(self._media_repeat)

        shuffle = init_status["random"]
        await self._icon_media_shuffle(shuffle)
        self.media_shuffle.clicked.connect(self._media_shuffle)
    
    async def __media_seek_init(self):
        client = self._idle_client
        self.media_seek.valueChanged.connect(self._media_seeker)
        while True:
            status = await client.status()
            duration = status.get("duration", 100)
            elapsed = status.get("elapsed", 0)
            
            self.media_seek.setMaximum(int(float(duration))) #FIXME Maybe should be placed elsewhere
            self.media_seek.setSliderPosition(int(float(elapsed)))
            
            await asyncio.sleep(0.5)

    async def _init_gui(self, init_status):
        await self.__playback_control_init(init_status)
        await self.__playlist_control_init(init_status)
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