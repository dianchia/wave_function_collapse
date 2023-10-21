import logging

from rich.logging import RichHandler

registered_logger = {}


def get_logger(name: str, level: str | int = logging.WARN) -> logging.Logger:
    if name in registered_logger:
        return registered_logger[name]

    formatter = logging.Formatter("%(message)s")
    handler = RichHandler(level, log_time_format="[%X]")
    logger = logging.getLogger(name)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False

    registered_logger[name] = logger
    return logger

