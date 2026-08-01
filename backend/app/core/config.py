from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pass

    class Config:
        env_file = ".env"

settings = Settings()