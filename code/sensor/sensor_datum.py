import time
from typing import Dict

class SensorDatum:
    def __init__(self):
        self.timestamp = time.time()


    def to_dict(self) -> Dict:
        return self.__dict__
