from pydantic import Field, AnyUrl

from storage.models.config.storage_config import StorageConfig


class InfluxDBConfig(StorageConfig):
    url: AnyUrl = Field(
        description="The URL of your InfluxDB instance"
    )
    organization: str = Field(
        description="The organization you want to write to"
    )
    bucket: str = Field(
        description="The bucket you want to write to"
    )
    api_token: str = Field(
        description="The API token you want to use"
    )
