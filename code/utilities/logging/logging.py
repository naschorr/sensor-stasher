import logging
import datetime
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

from utilities import *
from .log_level import LogLevel


class Logging:
    @staticmethod
    def initialize_logging(logger):
        config = load_config()

        FORMAT = "%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(FORMAT)
        logging.basicConfig(format=FORMAT)

        log_level = str(config.get("log_level", LogLevel.DEBUG)).lower()
        if (log_level == LogLevel.DEBUG):
            logger.setLevel(logging.DEBUG)
        elif (log_level == LogLevel.INFO):
            logger.setLevel(logging.INFO)
        elif (log_level == LogLevel.WARNING):
            logger.setLevel(logging.WARNING)
        elif (log_level == LogLevel.ERROR):
            logger.setLevel(logging.ERROR)
        elif (log_level == LogLevel.CRITICAL):
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.DEBUG)

        ## Get the directory containing the logs and make sure it exists, creating it if it doesn't
        log_path = config.get("log_path")
        if (log_path):
            log_path = Path(log_path)
        else:
            log_path = Path.joinpath(get_root_path(), 'logs')

        log_path.mkdir(parents=True, exist_ok=True)    # Basically a mkdir -p $log_path
        log_file = Path(log_path, 'sensor_stasher.log')    # Build the true path to the log file

        ## Windows has an issue with overwriting old logs (from the previous day, or older) automatically so just delete
        ## them. This is hacky, but I only use Windows for development so it's not a big deal.
        removed_previous_logs = False
        if ('nt' in os.name and log_file.exists()):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
            now = datetime.datetime.now()
            if (last_modified.day != now.day):
                os.remove(log_file)
                removed_previous_logs = True

        ## Setup and add the timed rotating log handler to the logger
        backup_count = config.get("log_backup_count", 7)    # Store a week's logs then start overwriting them
        log_handler = TimedRotatingFileHandler(str(log_file), when='midnight', interval=1, backupCount=backup_count)
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

        ## With the new logger set up, let the user know if the previously used log file was removed.
        if (removed_previous_logs):
            logger.info("Removed previous log file.")

        return logger