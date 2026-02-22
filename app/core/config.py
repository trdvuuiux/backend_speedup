import os
import yaml
from pathlib import Path

# Get project root (go up 2 levels: from core/ to app/ to project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load config from yaml
config_path = BASE_DIR / "config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)


class Settings:
    # App
    APP_NAME: str = config.get("app", {}).get("name", "Speed Up Backend")
    DEBUG: bool = config.get("app", {}).get("debug", True)

    # Database
    DB_HOST: str = config.get("database", {}).get("host", "localhost")
    DB_PORT: int = config.get("database", {}).get("port", 3306)
    DB_USER: str = config.get("database", {}).get("username", "root")
    DB_PASSWORD: str = config.get("database", {}).get("password", "12345678")
    DB_NAME: str = config.get("database", {}).get("name", "speed_up")

    # Database URL
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # JWT
    SECRET_KEY: str = config.get("jwt", {}).get("secret_key", "your-secret-key")
    ALGORITHM: str = config.get("jwt", {}).get("algorithm", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config.get("jwt", {}).get("access_token_expire_minutes", 30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config.get("jwt", {}).get("refresh_token_expire_days", 7)

    # Email
    SMTP_HOST: str = config.get("email", {}).get("smtp_host", "smtp.gmail.com")
    SMTP_PORT: int = config.get("email", {}).get("smtp_port", 587)
    SMTP_USER: str = config.get("email", {}).get("smtp_user", "")
    SMTP_PASSWORD: str = config.get("email", {}).get("smtp_password", "")


settings = Settings()
