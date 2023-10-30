import inspect
import importlib
import sys
from typing import Optional
from pathlib import Path

from utilities.logging.logging import Logging


class ImplementationFinder:
    ## Lifecycle

    def __init__(self):
        self.logger = Logging.LOGGER

    ## Methods

    def find_implementation_class(self, directory: Path, base_class: list[type]) -> Optional[type]:
        """
        Search the given directory for a Python file that contains a class that inherits from all of the given
        base_class classes
        """

        ## todo: we don't need to add the directory to the path every time, just once at the beginning and then remove
        ## it if nothing was found
        for file in directory.iterdir():
            ## Ignore non-Python files
            if (file.suffix != ".py"):
                continue

            ## Tentative import
            ## todo: too many strings are being added to the path, fix this
            sys.path.append(str(file.parent))
            try:
                candidate_module = importlib.import_module(file.stem)
            except Exception as e:
                ## todo remove this once all sensors have been ported over
                self.logger.debug(f"Unable to import module: {file.stem}, {e}")
                sys.path.remove(str(file.parent))
                continue

            ## Does this implementation class inherit from the expected base class(es)?
            implementation = None
            for _, cls in inspect.getmembers(candidate_module, inspect.isclass):
                if (
                        all(issubclass(cls, base) for base in base_class)   ## Must match ALL base classes
                        and cls is not base_class
                        and cls.__module__ == candidate_module.__name__
                ):
                    implementation = cls
                    break

            ## Clean up the module if it's not what we're looking for and start over with the next file
            if (implementation is None):
                del candidate_module
                sys.path.remove(str(file.parent))
                continue

            return implementation