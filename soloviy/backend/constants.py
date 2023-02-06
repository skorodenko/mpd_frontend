from os import path
from xdg import xdg_config_home

CONFIG_DIR = path.join(xdg_config_home, "soloviy")
APP_CONFIG_FILE = path.join(CONFIG_DIR, "soloviy.conf")

MPD_NATIVE_CONFIG_FILE = path.join(CONFIG_DIR, "mpd.conf")
MPD_NATIVE_SOCKET = path.join(CONFIG_DIR, "mpd.socket")

DEFAULT_APP_SETTINGS = {
    "mpd_socket": MPD_NATIVE_SOCKET,
}