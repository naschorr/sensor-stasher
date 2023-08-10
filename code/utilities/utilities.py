import json

import platform
from pathlib import Path
from typing import Optional

## Config
CONFIG_NAME = "config.json"	            # The name of the config file
DEV_CONFIG_NAME = "config.dev.json"     # The name of the dev config file (overrides properties stored in the normal and prod config files)
PROD_CONFIG_NAME = "config.prod.json"   # The name of the prod config file (overrides properties stored in the normal config file)
DIRS_FROM_ROOT = 2			            # How many directories away this script is from the root


def get_root_path() -> Path:
    path = Path(__file__)

    for _ in range(DIRS_FROM_ROOT + 1):  # the '+ 1' includes this script in the path
        path = path.parent

    return path


def load_json(path: Path) -> dict:
    with open(path) as fd:
        return json.load(fd)


def validate_system(wrapped):
    """
    Simple decorator to ensure that sub-methods will only run on supported systems.
    Right now, only the RaspberryPi is supported.
    """

    def wrapper(self):
        if (platform.uname().node != "raspberrypi"):
            raise NotImplementedError("Only RaspberryPi is supported at this time.")
        wrapped(self)

    return wrapper
