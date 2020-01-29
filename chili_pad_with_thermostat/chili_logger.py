import logging

class _ChiliLogger:
    LOGGER_NAME = 'chili_logger'

    def __init__(self):
        logger = logging.getLogger(_ChiliLogger.LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler('chili.log')
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)-15s %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    def get_logger(self):
        return logging.getLogger(_ChiliLogger.LOGGER_NAME)

    # 'application' code
        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warning('warn message')
        # logger.error('error message')
        # logger.critical('critical message')


def ChiliLogger():
    global _chili_logger
    try:
        _chili_logger
    except NameError:
        _chili_logger = _ChiliLogger()

    return _chili_logger
