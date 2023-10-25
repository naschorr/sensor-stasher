import platform
from pathlib import Path

from common.models.platform_type import PlatformType

## Config
DIRS_FROM_ROOT = 2			            # How many directories away this script is from the root


def get_root_path() -> Path:
    path = Path(__file__)

    for _ in range(DIRS_FROM_ROOT + 1):  # the '+ 1' includes this script in the path
        path = path.parent

    return path


def get_current_platform() -> PlatformType:
    if (platform.uname().node.lower() == "raspberrypi"):
        return PlatformType.RASPBERRYPI
    if (platform.uname().system.lower() == "windows"):
        return PlatformType.WINDOWS
    ## More as necessary

    raise RuntimeError("Unsupported platform")
