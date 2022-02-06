import logging

from logging import config

log_config = {
    "version": 1,
    "loggers": {
        "gb.client": {
            "handlers": ["file_out", "console"],
            "level": "DEBUG",
        },
    },
    "handlers": {
        "file_out": {
            "filename": "gb.client.log",
            "formatter": "default_formatter",
            "class": "logging.FileHandler",
            "level": "INFO"
        },
        "console": {
            "formatter": "default_formatter",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s - [%(levelname)s] - %(module)s - %(message)s ",
            "datefmt": "%d-%m-%Y %H:%M:%S"
        }
    },
}

config.dictConfig(log_config)

if __name__ == '__main__':
    log_config["handlers"]["console"] = {
        "formatter": "default_formatter",
        "class": "logging.StreamHandler",
        "level": "INFO"
    }
    log_config["loggers"]["gb.client"]["handlers"].append("console")
    config.dictConfig(log_config)
    logger = logging.getLogger('gb.client')
    logger.info('Test logging message')
