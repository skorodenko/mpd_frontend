import logging


logger = logging.getLogger(__name__)


def factory_mpd_binary() -> bool:
    from shutil import which

    binary = which("mpd")
    if binary:
        logger.debug(f"Found 'mpd' binary: {binary}")
    else:
        logger.debug("Mpd binary not found in PATH")
    return binary
