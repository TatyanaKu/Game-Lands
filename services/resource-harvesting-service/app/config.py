from pydantic import BaseSettings, PostgresDsn, Field

class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default='postgresql://user:pass@localhost:5432/foobar',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )
    

    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()

# from pydantic import BaseSettings, Field, FilePath
# class Config(BaseSettings):
#     config_path: FilePath = Field(
#         default='/config.json',
#         env='CONFIG_PATH',
#         alias='CONFIG_PATH',
#     )    