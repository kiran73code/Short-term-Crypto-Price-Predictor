from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """ "
    pydantic class for loading config parametrs
    """

    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str
