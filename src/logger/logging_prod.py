from logging.config import dictConfig


LOGGING_PROD = {  # type: ignore
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": ("%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(name)s | %(message)s")}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "errors": {
            "class": "logging.FileHandler",
            "filename": "errors.log",
            "encoding": "utf-8",
            "level": "ERROR",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "errors"],
    },
    "loggers": {
        "aiogram": {
            "level": "INFO",
        },
        "json_storage": {
            "level": "WARNING",
        },
    },
}


def setup_logging() -> None:
    dictConfig(LOGGING_PROD)  # type: ignore
