import logging
import logging.config
import copy
import inspect
import os
import sys
import socket


current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

class AppSettings:

    VERSION = '1.0'
    DATA_DIR = os.path.join(current_dir, "dst")
    TMP_DIR = os.path.join(current_dir, "tmp")
    TEMPLATE_FILE_DIR = os.path.join(current_dir, "templates")
    FastAPI_PORT = 8060

    # Logging config
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "infoFormat": {
                "format": "%(asctime)s - %(levelname)s - %(funcName)s: %(message)s",
                "datefmt": "%m/%d/%Y %H:%M:%S %p"
            },
            "errorFormat": {
                "format": "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "infoFormat"
            },
            "info": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "infoFormat",
                "mode": "a",
                "filename": os.path.join(DATA_DIR, "logs", "info.log"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "errorFormat",
                "mode": "a",
                "filename": os.path.join(DATA_DIR, "logs", "error.log"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "debug": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "info", "error"]
        }
    }

    @classmethod
    def configuration(cls) -> None:
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)

        if not os.path.exists(cls.TMP_DIR):
            os.makedirs(cls.TMP_DIR)

        cls.configure_logging(cls.DATA_DIR)

    @classmethod
    def configure_logging(cls, logDir: str) -> None:
        if not os.path.exists(os.path.join(logDir, "logs")):
            os.mkdir(os.path.join(logDir, "logs"))
        logging.config.dictConfig(cls.LOGGING)

    @classmethod
    def load_configuration(cls, config: dict) -> None:
        for key, value in config.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                logging.error(
                    f"Invaild attribute {key}. Please check your config file.")
                raise ValueError(
                    f"Invaild attribute {key}. Please check your config file.")

    @classmethod
    def to_dict(cls):
        output = {}
        skip = []

        for member, value in inspect.getmembers(cls):
            if not member.startswith("_") and not inspect.ismethod(value) and member not in skip:
                if not isinstance(value, dict):
                    output[member] = value
                else:
                    output[member] = copy.deepcopy(value)
        return output
    
    @classmethod
    def set_port(cls, port=8060, max_port=65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                logging.info(f"FastAPI will bind port: {port}")
                AppSettings.Framework_PORT = port

                return AppSettings.Framework_PORT
            except OSError:
                port += 1
        raise IOError('no free ports') 
