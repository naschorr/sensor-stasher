import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from common.models.config.sensor_stasher_config import SensorStasherConfig
from storage.models.storage_adapter import StorageAdapter
from storage.models.storage_type import StorageType
from storage.clients.influx_db.influx_db_config import InfluxDBConfig
from sensor.models.data.sensor_measurement import SensorMeasurement
from utilities.logging.logging import Logging


class InfluxDBClient(StorageAdapter):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, influx_db_configuration: InfluxDBConfig):
        self.logger = Logging.LOGGER

        ## Config
        self.system_type = sensor_stasher_configuration.system_type
        self.system_id = sensor_stasher_configuration.system_id
        self.url = str(influx_db_configuration.url)
        self.organization = influx_db_configuration.organization
        self.bucket = influx_db_configuration.bucket
        self.api_token = influx_db_configuration.api_token
        self._storage_type = StorageType.INFLUXDB

        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.api_token, org=self.organization)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

        self.logger.debug(f"Initialized InfluxDB client. url: '{self.url}', organization: '{self.organization}', bucket: '{self.bucket}'")

    ## Properties

    @property
    def storage_type(self) -> StorageType:
        return self._storage_type

    ## Methods

    def _build_points_from_data(self, data: SensorMeasurement) -> list[influxdb_client.Point]:
        category = data.metadata.get('category')
        sensor_name = data.metadata.get('sensor_name')
        sensor_id = data.metadata.get('sensor_id')
        timestamp = data.metadata.get('timestamp')

        points: list[influxdb_client.Point] = []

        for key, value in data.to_dict().items():
            point = influxdb_client.Point(category) \
                .tag("system_type", self.system_type) \
                .tag("system_id", self.system_id) \
                .tag("sensor_name", sensor_name) \
                .tag("sensor_id", sensor_id) \
                .time(timestamp) \
                .field(key, value)

            points.append(point)

        return points


    def store(self, data: list[SensorMeasurement]):
        points = []
        for datum in data:
            points.extend(self._build_points_from_data(datum))

        self.write_api.write(self.bucket, self.organization, points)
