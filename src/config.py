import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
    )

    DEBUG: bool = False
    SECRET_KEY: str = "32198"
    BASE_DIR: str = os.path.dirname(__file__)
    print(os.getenv('BOT_TOKEN'))
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')




app_settings = BotSettings()
