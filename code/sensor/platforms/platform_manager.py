from typing import Type

from models.platform_type import PlatformType
from sensor.platforms.configurations.platform_config import PlatformConfig
from sensor.platforms.configurations.raspberrypi_config import RaspberryPiConfig
from sensor.platforms.configurations.windows_config import WindowsConfig
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from sensor.platforms.sensors.agnostic_sensor import AgnosticSensor
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.platforms.sensors.windows_sensor import WindowsSensor


class PlatformManager:
    @staticmethod
    def get_platform_sensor(platform_type: PlatformType) -> Type[PlatformSensor]:
        if (platform_type == PlatformType.AGNOSTIC):
            return AgnosticSensor
        if (platform_type == PlatformType.RASPBERRYPI):
            return RaspberryPiSensor
        if (platform_type == PlatformType.WINDOWS):
            return WindowsSensor

        raise RuntimeError(f"Platform type {platform_type} not supported")


    @staticmethod
    def get_platform_config(platform_type: PlatformType) -> Type[PlatformConfig]:
        if (platform_type == PlatformType.RASPBERRYPI):
            return RaspberryPiConfig
        if (platform_type == PlatformType.WINDOWS):
            return WindowsConfig

        raise RuntimeError(f"Platform type {platform_type} not supported")
