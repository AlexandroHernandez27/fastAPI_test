# Standard Library
import logging
from logging.config import dictConfig
from pydantic import BaseModel
from .base import Settings


class LogConfig(BaseModel):
    LOG_FORMAT: str = "%(levelprefix)s \033[36m\033[1m[%(asctime)s | %(name)s:%(lineno)d]: \033[0m%(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "": {"handlers": ["default"], "level": LOG_LEVEL},
    }


log_config_dict = LogConfig().__dict__
dictConfig(LogConfig().model_dump())


log = logging.getLogger(__name__)
settings: Settings = Settings()

