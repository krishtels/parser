from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
