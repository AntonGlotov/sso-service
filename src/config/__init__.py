from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_PATH:str = "../data/user.sqlite3"

    LOG_PATH: str = "../logs/logs.log"
    LOG_LEVEL: str = "INFO"

    HOST: str = "localhost"
    PORT: int = 8000

    class Config:
        env_file = "../config/.env"


settings = Settings()