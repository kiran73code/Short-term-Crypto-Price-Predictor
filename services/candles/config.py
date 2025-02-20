from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """pydantic class for loading configuration parametrs"""

    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int
    emit_incomplete_candles: Optional[bool] = True
    data_source: Literal['live', 'historical', 'test']


config = Config()
