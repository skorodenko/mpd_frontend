from os import path
from xdg import xdg_config_home

CONFIG_HOME = xdg_config_home()
CONFIG_DIR = path.join(CONFIG_HOME, "soloviy")
APP_CONFIG_FILE = path.join(CONFIG_DIR, "soloviy.conf")

MPD_NATIVE_CONFIG_FILE = path.join(CONFIG_DIR, "mpd.conf")
MPD_NATIVE_SOCKET = path.join(CONFIG_DIR, "mpd.socket")

APP_DEFAULT_SETTINGS = {
    "mpd_socket": "",
    "tiling_mode":"2",
    "playlists_margin": "2",
}