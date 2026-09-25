import sys
from enum import Enum

from loguru import logger

from .context import AppContext
from .router import Router


class Levels(Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


def logger_init():
    logger.remove(0)
    logger.add(sys.stderr, level=Levels.info.value)


def main():
    context = AppContext()
    router = Router(context)
    router.run()


if __name__ == "__main__":
    logger_init()
    main()
