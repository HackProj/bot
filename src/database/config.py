from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix='DB__'
    )
    HOST: str = "localhost"
    PORT: str = "5432"
    NAME: str = "bot_db"
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    POOL_SIZE: int = 5
    MAX_OWERFLOW: int = 10

    @property
    def db_settings(self):
        return self

    def get_dsn_async(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}' \
               f'@{self.HOST}:{self.PORT}/{self.NAME}'

    def get_dsn_sync(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}' \
               f'@{self.HOST}:{self.PORT}/{self.NAME}'


db_settings = DBSettings()
