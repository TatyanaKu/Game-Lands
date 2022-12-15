from pydantic import BaseSettings, Field, FilePath

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


#переменная GAMEPLAY_SERVICE_ENTRYPOINT проверка уровней через ip 192.168.0.2:5000 (в файле config.py) 