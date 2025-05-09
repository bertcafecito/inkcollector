import logging
from logging.handlers import RotatingFileHandler
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": "logs/inkcollector.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
        },
    },
    "loggers": {
        "inkcollector": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logger(name, level=logging.INFO, log_file="inkcollector.log"):
    """
    Sets up logging using the configuration dictionary.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger("inkcollector")
