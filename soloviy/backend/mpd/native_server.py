from soloviy.backend.constants import MPD_NATIVE_CONFIG_FILE, MPD_NATIVE_SOCKET
from subprocess import Popen

def native_mpd(socket):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if socket == MPD_NATIVE_SOCKET: 
                with Popen(["mpd", MPD_NATIVE_CONFIG_FILE]) as mpd_process:
                    f(*args, **kwargs)
            else:
                f(*args, **kwargs)
        return wrapper
    return decorator