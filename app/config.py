import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Rate Limiter Service"
    debug: bool = True
    database_url: str = "sqlite:///./rate_limiter.db"
    
    class Config:
        env_file = ".env"


settings = Settings()