import inspect
import contextlib
import pydantic
from typing import TypeVar, Union, Optional

from common.exceptions.instantiation_exception import InstantiationException
from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.models.config.sensor_config import SensorConfig
from stasher.models.storage_adapter import StorageAdapter
from stasher.models.config.storage_config import StorageConfig
from utilities.logging.logging import Logging

## Generics to keep this clean
ImplementationClass = TypeVar("ImplementationClass", bound=Union[SensorAdapter, StorageAdapter])
ConfigurationClass = TypeVar("ConfigurationClass", bound=Union[SensorConfig, StorageConfig])


class ImplementationInstantiator:
    ## Lifecycle

    def __init__(self, logger: Logging, sensor_stasher_configuration: SensorStasherConfig):
        self.logger = logger
        self.sensor_stasher_configuration = sensor_stasher_configuration

    ## Methods

    def _configuration_retriever(
            self,
            configuration_class: ConfigurationClass,
            configuration_pool: pydantic.BaseModel
    ) -> Optional[ConfigurationClass]:
        """
        Attempts to find a configuration property with the same type as the provided sensor configuration class.
        For example: the PMS7003Config sensor config would yield the pms7003 property of the Configuration class.
        """

        for _, cls in inspect.getmembers(configuration_pool):
            with contextlib.suppress(TypeError, AttributeError):
                ## todo: Improve this. `isinstance` wasn't really playing nice for the following:
                ## sensor_config: <class 'ds18b20_config.DS18B20Config'> and
                ## cls: DS18B20Config(...). I'm sure it's something simple though

                if (
                        hasattr(cls, "__module__") and
                        cls.__module__ is not None and
                        cls.__module__.endswith(configuration_class.__module__)
                ):
                    return cls

        return None


    def _instantiate_class(
            self,
            implementation_class: ImplementationClass,
            configuration_class: ConfigurationClass,
            configuration_pool: pydantic.BaseModel
    ) -> SensorAdapter:
        """
        Handles instantiating from a given implementation class and configuration class. Assumes implementations simply
        take a configuration parameter
        """

        ## If we found a configuration class, use that to find the actual processed configuration class of the same type
        configuration = None
        if (configuration_class is not None):
            configuration = self._configuration_retriever(configuration_class, configuration_pool)

        ## Extract the parameters used to instantiate the class
        parameters = [parameter for name, parameter in inspect.signature(implementation_class.__init__).parameters.items()]

        ## Does it have the wrong number of parameters?
        if (len(parameters) != 3):
            raise InstantiationException(f"Invalid number of parameters for class: {implementation_class.__name__}")

        ## Does it have the expected number of parameters?
        if (len(parameters) == 3):
            ## Make sure we've got a configuration class to work with
            if (configuration is None):
                raise InstantiationException(f"No configuration file provided for class: {implementation_class.__name__}")

            ## Are the parameters of the expected type? (Don't try and instantiate a sensor that's expecting an int)
            if (
                    (
                        parameters[1].annotation is None or
                        (
                            parameters[1].annotation is not None and
                            not issubclass(parameters[1].annotation, SensorStasherConfig)
                        )
                    ) and (
                        parameters[2].annotation is None or
                        (
                            parameters[2].annotation is not None and
                            not issubclass(parameters[2].annotation, ConfigurationClass)
                        )
                    )
            ):
                raise InstantiationException(f"Invalid parameter type for class: {implementation_class.__name__}.")
            
            ## We're all clear to instantiate
            return implementation_class(self.sensor_stasher_configuration, configuration) # type: ignore


    def instantiate_classes(
            self,
            class_config_map: dict[ImplementationClass, ConfigurationClass],
            configuration_pool: pydantic.BaseModel
    ) -> set[ImplementationClass]:
        """
        Initialize the available sensors, and inject the relevant configuration property into them (if it exists). Note
        that issues with sensor initialization won't stop the rest from initializing.
        """

        instantiated_classes = set()
        for implementation_class, configuration_class in class_config_map.items():
            try:
                instantiated_class = self._instantiate_class(implementation_class, configuration_class, configuration_pool)
                instantiated_classes.add(instantiated_class)
                self.logger.info(f"Successfully initialized class: '{instantiated_class.__class__.__name__}'")
            except InstantiationException as e:
                ## Couldn't instantiate? No worries, just ignore it and move on
                self.logger.warn(f"Unable to initialize class: '{implementation_class.__name__}' - {e}")
                continue

        return instantiated_classes
