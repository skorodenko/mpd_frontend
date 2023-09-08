import logging.config
from soloviy.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {
            "level": settings.logging.level,
            "propagate": False,
            "handlers": ["stream_handler"],
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default_formatter",
        },
#        "file_handler": {
#            "class": "logging.FileHandler",
#            "filename": settings.log_file,
#            "mode": "w",
#            "level": "DEBUG",
#            "formatter": "default_formatter",
#        },
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s-%(levelname)s :: %(name)s :: %(module)s [%(message)s]",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)