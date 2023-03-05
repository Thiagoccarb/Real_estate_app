import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

API_DB_HOST = os.getenv("API_DB_HOST")
API_DB_USER = os.getenv("API_DB_USER")
API_DB_PASSWORD = os.getenv("API_DB_PASSWORD")
API_DB_DATABASE = os.getenv("API_DB_DATABASE")


class Settings(BaseSettings):
    class Config:
        env_file = f".env"

    # Application
    NAME: str = "real-state API"
    APPLICATION_NAME: str = "real-state-api"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "real-state API in Python"

    # Environment
    PYTHON_ENVIRONMENT: str = os.getenv("PYTHON_ENVIRONMENT", "local")

    # Database
    API_DB_HOST: str = API_DB_HOST
    API_DB_USER: str = API_DB_USER
    API_DB_PASSWORD: str = API_DB_PASSWORD
    API_DB_DATABASE: str = API_DB_DATABASE


settings = Settings()
