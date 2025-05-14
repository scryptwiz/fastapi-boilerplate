import logging
from enum import StrEnum

# LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
LOG_FORMAT_DEBUG = "%(asctime)s: %(levelname)s: %(pathname)s - %(funcName)s - Line %(lineno)d - %(message)s"
LOG_FORMAT_DEFAULT = "%(asctime)s: %(levelname)s: %(message)s"

class LogLevels(StrEnum):
    info = "INFO"
    debug = "DEBUG"
    warning = "WARNING"
    error = "ERROR"

def configure_logging(log_level: str = LogLevels.error, log_to_file: bool = False ):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=logging.ERROR)
        return

    log_format = LOG_FORMAT_DEBUG if log_level == LogLevels.debug.value else LOG_FORMAT_DEFAULT
    log_file = "app.log" if log_to_file else None

    handlers = [logging.StreamHandler()]
    if log_to_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)

    logging.debug(f"Logging configured at level: {log_level}")