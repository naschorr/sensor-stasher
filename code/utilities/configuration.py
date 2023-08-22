import json
from pathlib import Path
from typing import Optional

from models.config.sensor_stasher_config import SensorStasherConfig
from utilities.misc import get_root_path


class Configuration:
    CONFIG_NAME = "config.json"	            # The name of the config file
    PROD_CONFIG_NAME = "config.prod.json"   # The name of the prod config file
    DEV_CONFIG_NAME = "config.dev.json"     # The name of the dev config file


    @staticmethod
    def _load_config_hierarchy(directory_path: Optional[Path] = None) -> dict:
        """
        Loads configuration data from the given directory (or the app's root if not provided) into a dictionary. The
        expected prod, dev, and config configuration files are loaded separately and combined into the same dict under
        different keys ("dev", "prod", "config").

        :param directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type directory_path: Path, optional
        :return: Dictionary containing individual dev, prod, and root config items.
        :rtype: dict
        """

        def load_json(path: Path) -> dict:
            with open(path) as fd:
                return json.load(fd)


        path = directory_path or get_root_path()
        config = {}

        dev_config_path = Path.joinpath(path, Configuration.DEV_CONFIG_NAME)
        if (dev_config_path.exists()):
            config["dev"] =  load_json(dev_config_path)

        prod_config_path = Path.joinpath(path, Configuration.PROD_CONFIG_NAME)
        if (prod_config_path.exists()):
            config["prod"] = load_json(prod_config_path)

        config_path = Path.joinpath(path, Configuration.CONFIG_NAME)
        if (config_path.exists()):
            config["config"] = load_json(config_path)

        return config


    @staticmethod
    def _build_config_hierarchy(directory_path: Optional[Path] = None) -> dict:
        """
        Parses one or more JSON configuration files to build a dictionary with proper precedence for configuring the
        program. Dev configurations take priority over prod configurations, which take priority over root level
        configurations.

        :param directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type directory_path: Path, optional
        :return: A dictionary containing key-value pairs for use in configuring parts of the program.
        :rtype: dict
        """

        config_chunks = Configuration._load_config_hierarchy(directory_path or get_root_path())

        config  = config_chunks.get("config", {})
        config |= config_chunks.get("prod", {})
        config |= config_chunks.get("dev", {})

        return config


    @staticmethod
    def load_configuration(directory_path: Optional[Path] = None) -> SensorStasherConfig:
        """
        Loads the configuration file from the provided directory (or the app's root if not provided) and returns a
        validated SensorStasherConfig object.

        :param directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type directory_path: Path, optional
        :return: SensorStasherConfig object containing the validated configuration data.
        :rtype: SensorStasherConfig
        """

        config = Configuration._build_config_hierarchy(directory_path)

        return SensorStasherConfig(**config)
