import logging

_LOGGER = None


def get_logger():
    global _LOGGER
    if _LOGGER is None:
        # logging.basicConfig(format="[%(levelname) %(name)] %(asctime) %(message)", datefmt="%H:$M:%S",level=logging.DEBUG)
        logging.basicConfig(format="[%(asctime)s %(levelname)-5s]: %(message)s", datefmt="%H:%M:%S",level=logging.DEBUG)
        # logging.basicConfig(level=logging.DEBUG)
        _LOGGER = logging.getLogger("")
        _LOGGER.info("Started logging")
    return _LOGGER
