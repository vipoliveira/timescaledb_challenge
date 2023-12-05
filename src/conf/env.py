from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    POSTGRES_DBNAME: str = 'stocks'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_prefix='ENV_')