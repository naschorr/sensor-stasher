import logging
import datetime
import os
from logging.handlers import TimedRotatingFileHandler

from common.models.platform_type import PlatformType
from utilities.logging.logging_config import LoggingConfig
from utilities.misc import get_current_platform
from .log_level import LogLevel


class Logging:

    ## Statics

    ## todo: not static, just inject the same Logging instance into classes that need to log data
    LOGGER = None

    ## Lifecycle

    def __init__(self, logging_config: LoggingConfig):
        ## todo: simplify log level configuration
        self.log_level = logging_config.log_level
        self.log_path = logging_config.log_path
        self.log_backup_count = logging_config.log_backup_count
        self.log_name = logging_config.log_name

        if (not Logging.LOGGER):
            Logging.LOGGER = self._initialize_logging()

    ## Properties

    @property
    def logger(self):
        return Logging.LOGGER

    ## Methods

    def _initialize_logging(self) -> logging.Logger:
        ## Basic logger init
        logger = logging.getLogger()
        log_format = "%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        logging.basicConfig(format=log_format)

        ## Set the log level
        if (self.log_level == LogLevel.DEBUG):
            logger.setLevel(logging.DEBUG)
        elif (self.log_level == LogLevel.INFO):
            logger.setLevel(logging.INFO)
        elif (self.log_level == LogLevel.WARNING):
            logger.setLevel(logging.WARNING)
        elif (self.log_level == LogLevel.ERROR):
            logger.setLevel(logging.ERROR)
        elif (self.log_level == LogLevel.CRITICAL):
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.DEBUG)

        ## Get the directory containing the logs and make sure it exists, creating it if it doesn't
        self.log_path.mkdir(parents=True, exist_ok=True)    # Basically a mkdir -p $log_path
        log_file = self.log_path / (self.log_name + ".log")    # Build the true path to the log file

        ## Windows has an issue with overwriting old logs (from the previous day, or older) automatically so just delete
        ## them. This is hacky, but I only use Windows for development so it's not a big deal.
        removed_previous_logs = False
        if (get_current_platform() == PlatformType.WINDOWS and log_file.exists()):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
            now = datetime.datetime.now()
            if (last_modified.day != now.day):
                os.remove(log_file)
                removed_previous_logs = True

        ## Setup and add the timed rotating log handler to the logger
        log_handler = TimedRotatingFileHandler(str(log_file), when='midnight', interval=1, backupCount=self.log_backup_count)
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

        ## With the new logger set up, let the user know if the previously used log file was removed.
        if (removed_previous_logs):
            logger.info("Removed previous log file.")

        return logger