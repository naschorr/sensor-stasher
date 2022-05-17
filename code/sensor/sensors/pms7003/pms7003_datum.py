from typing import Dict

from sensor.sensor_datum import SensorDatum
from sensor.sensor_categories import SensorCategories


class PMS7003Datum(SensorDatum):
    def __init__(self, sensor_category: SensorCategories, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(sensor_category, sensor_type, sensor_id)

        ## PM1.0 thru PM10 CF=1, standard particle
        self.pm1_0cf1 = measurement.get('pm1_0cf1')
        self.pm2_5cf1 = measurement.get('pm2_5cf1')
        self.pm10cf1 = measurement.get('pm10cf1')

        ## PM1.0 thru PM10 atmospheric environment
        self.pm1_0sat = measurement.get('pm1_0')
        self.pm2_5sat = measurement.get('pm2_5')
        self.pm10sat = measurement.get('pm10')

        ## Number of particles in the air with size greater than N um
        self.n0_3 = measurement.get('n0_3')
        self.n0_5 = measurement.get('n0_5')
        self.n1_0 = measurement.get('n1_0')
        self.n2_5 = measurement.get('n2_5')
        self.n5_0 = measurement.get('n5_0')
        self.n10 = measurement.get('n10')
