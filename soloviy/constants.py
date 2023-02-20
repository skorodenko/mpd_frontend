from os import path
from xdg import xdg_config_home

CONFIG_HOME = xdg_config_home()
CONFIG_DIR = path.join(CONFIG_HOME, "soloviy")
APP_CONFIG_FILE = path.join(CONFIG_DIR, "soloviy.conf")

MPD_NATIVE_CONFIG_FILE = path.join(CONFIG_DIR, "mpd.conf")
MPD_NATIVE_SOCKET = path.join(CONFIG_DIR, "mpd.socket")

APP_DEFAULT_SETTINGS = {
    #"mpd_socket": None,
    "mpd_socket":"/home/rinkuro/.local/share/cantata/mpd/socket",
    "media_repeat": "single", #TODO Should be "no"
    "media_shuffle": "no",
    "playlists_mode":"1",
    "playlists_margin": "2",
}