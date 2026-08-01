from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Custom PC Builder API"
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()