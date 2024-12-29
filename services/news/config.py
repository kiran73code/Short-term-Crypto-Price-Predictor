from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptopanicCredentials(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='cryptonic_credentials.env', env_file_encoding='utf-8'
    )
    api_key: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_topic: str
    polling_interval_sec: int


config = Config()
cryptopanic_credentials = CryptopanicCredentials()
