import attrs
import logging
import qtinter
import pathlib
import datetime
import asyncio
from soloviy.config import settings
from soloviy.frontend.qmodels import PlaylistsModel
from soloviy.frontend.widgets.init_wizard import InitWizard
from soloviy.frontend.widgets.settings import Settings
from PySide6.QtGui import QActionGroup, QAction, QIcon, QPixmap, QFont
from PySide6.QtCore import QDir, QTimer, Signal, Slot, QProcess, QObject
from PySide6.QtWidgets import QMainWindow, QDialog, QApplication


@attrs.define
class Root(QObject):
    backend: QProcess = attrs.field(init=False)
    init_wizard: InitWizard = attrs.Factory(InitWizard, takes_self=True)
    settings: Settings = attrs.Factory(Settings, takes_self=True)

    def __attrs_pre_init__(self):
        super().__init__()
        QDir.addSearchPath("icons", "./soloviy/ui/icons/")
        self.setupUi(self)

    def __attrs_post_init__(self):
        ...
        # asyncio.create_task(self.backend.serve())
        # self._bind_signals()
        # self._init_state()
        # self._ui_post_init()
        # self._bind_buttons()

    def serve(self):
        # logger.info("Started main window")
        self.timer.singleShot(0, self.show)
        self.timer.singleShot(150, self._initial_configuration)

    def _initial_configuration(self):
        # logger.info("Started initial configuration")
        if not settings.mpd.socket:
            if self.init_wizard.exec() == QDialog.DialogCode.Rejected:
                self.close()
            else:
                self.update_db.emit()
                # self.settings.persist_settings()
        else:
            self.init_wizard.connect_mpd.emit(settings.mpd.socket)

    @backend.default
    def _start_backend(self):
        backend = QProcess()
        backend.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
        backend.start("python", ["-m", "soloviy.backend.main"])
        return backend

    #    def _init_state(self):
    #        logger.debug("Initializing state variables")
    #        if not state.get("group_by", None):
    #            state["group_by"] = settings.default.group_by
    #        if state.get("prev_tile"):
    #            state["prev_tile"] = None
    #
    #    def _ui_post_init(self):
    #        # Init menubar actions [Group by]
    #        group = state["group_by"]
    #        self.group_by_actions = QActionGroup(self)
    #        self.group_by_actions.setExclusive(True)
    #        self.group_by_actions.triggered.connect(self.__group_by_changed)
    #        actions = [self.actionDirectory, self.actionAlbum, self.actionAlbumartist,
    #                   self.actionArtist, self.actionComposer, self.actionDate,
    #                   self.actionFormat, self.actionGenre]
    #        for a in actions:
    #            if group == a.text().lower():
    #                a.setChecked(True)
    #            self.group_by_actions.addAction(a)
    #
    #        # Font setup
    #        light_font = QApplication.font()
    #        light_font.setWeight(QFont.Weight.Light)
    #        self.label_time.setFont(light_font)
    #        self.label_author.setFont(light_font)
    #        self.label_info.setFont(light_font)

    @Slot(str, dict)
    def __mpd_idle_update(self, field: str, status: dict):
        match field:
            case "state":
                match status["state"]:
                    case "play":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-pause")
                        )
                    case "pause":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-start")
                        )
                    case "stop":
                        self.media_play_pause.setIcon(
                            QIcon.fromTheme("media-playback-start")
                        )

            case "repeat" | "single":
                match status["repeat"], status["single"]:
                    case ("0", "0") | ("0", "1"):  # Second variant is redundant
                        self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-none"))
                    case ("1", "0"):
                        self.media_repeat.setIcon(QIcon.fromTheme("media-repeat-all"))
                    case ("1", "1"):
                        self.media_repeat.setIcon(
                            QIcon.fromTheme("media-repeat-single")
                        )

            case "random":
                if status["random"] == "0":
                    self.media_shuffle.setIcon(QIcon.fromTheme("media-playlist-normal"))
                else:
                    self.media_shuffle.setIcon(
                        QIcon.fromTheme("media-playlist-shuffle")
                    )

    @staticmethod
    def strfdelta(tdelta):
        h, rem = divmod(tdelta.seconds, 3600)
        m, s = divmod(rem, 60)
        match h, m, s:
            case h, _, _ if h != 0:
                return f"{h}:{m:0>2}:{s:0>2}"
            case _:
                return f"{m:0>2}:{s:0>2}"

    @Slot(int, int)
    def __update_seeker(self, duration: int, elapsed: int):
        dd = datetime.timedelta(seconds=duration)
        ed = datetime.timedelta(seconds=elapsed)

        self.label_time.setText(f"{self.strfdelta(ed)}/{self.strfdelta(dd)}")
        if self.media_seek.maximum() != duration:
            self.media_seek.setMaximum(duration)
        self.media_seek.setSliderPosition(elapsed)

    @Slot(dict, QPixmap)
    def __song_changed(self, info: dict, cover: QPixmap):
        title = info.get("title", "Title")
        artist = info.get("artist", "Artist")
        album = info.get("album", "Album")
        form = info.get("format", "0:0:0")
        freq, bitr, _ = form.split(":")
        file = info.get("file", "blank.ext")
        _, ext = pathlib.Path(file).suffix.upper().split(".")
        self.label_title.setText(title)
        self.label_author.setText(f"{artist} | {album}")
        self.label_info.setText(f"{int(freq)/1000} kHz, {bitr} bit, {ext}")
        self.label_art.setPixmap(cover)

    #    @Slot(QAction)
    #    def __group_by_changed(self, action: QAction):
    #        group = action.text().lower()
    #        state["group_by"] = group
    #        self.update_ui.emit()

    #    @Slot()
    #    def __update_playlists_view(self):
    #        logger.debug("Updating playlists view")
    #        group = state.get("group_by", settings.default.group_by)
    #        sql_group = getattr(db.Library, group)
    #        query = (db.Library
    #                    .select(sql_group)
    #                    .order_by(sql_group)
    #                    .distinct())
    #        playlists = [getattr(i, group) for i in query]
    #        playlists_model = PlaylistsModel(playlists)
    #        self.playlists_view.setModel(playlists_model)

    def closeEvent(self, event):
        # logger.info("Closing main window")
        self.backend.terminate()
        self.backend.waitForFinished(-1)
        super().closeEvent(event)
