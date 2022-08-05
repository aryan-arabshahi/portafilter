from logging import LoggerAdapter, StreamHandler, Formatter, DEBUG, Logger as MainLogger, getLogger
from datetime import datetime


class Logger(LoggerAdapter):

    def __init__(self, logger: MainLogger, extra=None):
        super(Logger, self).__init__(logger, extra or {})

    @staticmethod
    def setup(debug_mode: bool = False) -> None:
        """Setup a custom format for the logger
        """
        handler = StreamHandler()
        formatter = Formatter("%(levelname)s:%(name)s:%(message)s")
        handler.setFormatter(formatter)

        logger = getLogger('portafilter')

        if debug_mode:
            logger.setLevel(DEBUG)

        logger.addHandler(handler)

    def process(self, msg, kwargs):
        return f"[{str(datetime.now())}][{self.extra.get('prefix', '')}] - {msg}", kwargs
