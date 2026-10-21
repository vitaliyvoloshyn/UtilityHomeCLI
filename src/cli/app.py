import sys
from enum import Enum

from loguru import logger


class Levels(Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


def logger_init():
    logger.remove(0)
    logger.add(sys.stderr, level=Levels.debug.value)


logger_init()


from .context import AppContext
from .router import Router


def main():
    context = AppContext()
    router = Router(context)
    router.run()


if __name__ == "__main__":
    main()
