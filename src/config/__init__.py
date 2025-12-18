from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


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

    HOST: str = "localhost"
    PORT: int = 8000

    @property
    def project_root(self) -> str:
        return str(Path(__file__).parent.parent.parent)

    @property
    def database_path(self) -> str:
        return f"{self.project_root}/data/user.sqlite3"

    @property
    def pem_path_private(self) -> str:
        return f"{self.project_root}/secrets/private.pem"

    @property
    def pem_path_public(self) -> str:
        return f"{self.project_root}/secrets/public.pem"

    @property
    def log_path(self) -> str:
        return f"{self.project_root}/logs/logs.log"

    model_config = SettingsConfigDict(
        env_file=f"{str(Path(__file__).parent.parent.parent)}/secrets/.env"
    )


settings = Settings()
