from abc import ABC, abstractmethod
from typing import Dict


class SensorAdapter(ABC):
    @abstractmethod
    async def read(self) -> Dict:
        pass
