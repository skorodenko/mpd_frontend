from mpd import MPDClient
from soloviy.backend.app_config import config
from .native_server import native_mpd

MPD_SOCKET = config.get("mpd_socket")

@native_mpd(socket=MPD_SOCKET)    
def _mpd_client():
    client = MPDClient()
    client.connect(MPD_SOCKET)
    return client


client = _mpd_client()