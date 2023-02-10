from os import path
from xdg import xdg_config_home

CONFIG_HOME = xdg_config_home()
CONFIG_DIR = path.join(CONFIG_HOME, "soloviy")
APP_CONFIG_FILE = path.join(CONFIG_DIR, "soloviy.conf")

MPD_NATIVE_CONFIG_FILE = path.join(CONFIG_DIR, "mpd.conf")
MPD_NATIVE_SOCKET = path.join(CONFIG_DIR, "mpd.socket")

APP_DEFAULT_SETTINGS = {
    "mpd_socket": MPD_NATIVE_SOCKET, #TODO Should be None
    "media_repeat": "no",
    "media_shuffle": "no",
}