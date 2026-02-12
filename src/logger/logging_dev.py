from logging.config import dictConfig


LOGGING_DEV = {  # type: ignore
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": ("%(log_color)s%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(message)s"),
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
    "loggers": {
        "aiogram": {
            "level": "INFO",
        },
        "json_storage": {
            "level": "DEBUG",
        },
    },
}


def setup_logging() -> None:
    dictConfig(LOGGING_DEV)  # type: ignore
