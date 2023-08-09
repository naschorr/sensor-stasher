import json

from sensor.sensors.ds18b20.ds18b20_config import DS18B20Config
from sensor.sensors.pms7003.pms7003_config import PMS7003Config
from sensor.sensors.sht31.sht31_config import SHT31Config


# print(json.dumps(DS18B20Config.model_json_schema(), indent=2))
# print(json.dumps(PMS7003Config.model_json_schema(), indent=2))
print(json.dumps(SHT31Config.model_json_schema(), indent=2))
