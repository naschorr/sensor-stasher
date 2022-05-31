from pathlib import Path
from typing import List
import logging
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from storage.storage_adapter import StorageAdapter
from sensor.sensor_datum import SensorDatum
from utilities import load_config, initialize_logging

class InfluxDBClient(StorageAdapter):
    def __init__(self, system_type: str, system_id: str):
        config = load_config(Path(__file__).parent)
        self.logger = initialize_logging(logging.getLogger(__name__))

        self.url = config.get('url')
        self.api_token = config.get('api_token')
        self.organization = config.get('organization')
        self.bucket = config.get('bucket')
        self.system_type = system_type
        self.system_id = system_id

        self._storage_type = 'InfluxDB'

        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.api_token, org=self.organization)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

        self.logger.debug(f"Initialized InfluxDB client. url: '{self.url}', organization: '{self.organization}', bucket: '{self.bucket}'")

    ## Properties

    @property
    def storage_type(self) -> str:
        return self._storage_type

    ## Methods

    def _build_points_from_data(self, data: SensorDatum) -> List[influxdb_client.Point]:
        category = data.metadata.get('category')
        sensor_type = data.metadata.get('sensor_type')
        sensor_id = data.metadata.get('sensor_id')
        timestamp = data.metadata.get('timestamp')

        points: List[influxdb_client.Point] = []

        for key, value in data.to_dict().items():
            point = influxdb_client.Point(category) \
                .tag("system_type", self.system_type) \
                .tag("system_id", self.system_id) \
                .tag("sensor_type", sensor_type) \
                .tag("sensor_id", sensor_id) \
                .time(timestamp) \
                .field(key, value)

            points.append(point)

        return points


    def store(self, data: List[SensorDatum]):
        points = []
        for datum in data:
            points.extend(self._build_points_from_data(datum))

        self.write_api.write(self.bucket, self.organization, points)
