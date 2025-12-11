from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    SECRET_KEY: str
    PASSPHRASE: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_PATH:str = "../data/user.sqlite3"

    PEM_PATH_PRIVATE:str = "../secrets/private.pem"
    PEM_PATH_PUBLIC:str = "../secrets/public.pem"

    LOG_PATH: str = "../logs/logs.log"
    LOG_LEVEL: str = "INFO"

    HOST: str = "localhost"
    PORT: int = 8000

    class Config:
        env_file = "../secrets/.env"

settings = Settings()
