from pydantic import BaseSettings, PostgresDsn, Field, FilePath

class Config(BaseSettings):
    config_path: FilePath = Field(
        default='/config.json',
        env='CONFIG_PATH',
        alias='CONFIG_PATH',
    )
    
    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()
