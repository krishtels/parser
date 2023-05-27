from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class TwitchSettings(BaseSettings):
    TWITCH_CLIENT_ID: str
    TWITCH_SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
twitch_settings = TwitchSettings()
