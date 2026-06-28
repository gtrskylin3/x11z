from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
ENV_FILE = BASE_DIR / ".env"

db_path = (BASE_DIR / "english_app.db").resolve()

DB_URL = f"sqlite+aiosqlite:///{db_path.as_posix()}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )
    PORT: int
    RELOAD: bool
    HOST: str
    EMAIL: str
    API_URL: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )
    URL: str = DB_URL


settings = Settings() # type: ignore
db_settings = DatabaseSettings()

