import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

API_DB_HOST = os.getenv("API_DB_HOST")
API_DB_USER = os.getenv("API_DB_USER")
API_DB_PASSWORD = os.getenv("API_DB_PASSWORD")
API_DB_DATABASE = os.getenv("API_DB_DATABASE")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
BASE_URL: str = os.getenv("BASE_URL")


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

    # Url
    BASE_URL: str = BASE_URL

    # Database
    API_DB_HOST: str = API_DB_HOST
    API_DB_USER: str = API_DB_USER
    API_DB_PASSWORD: str = API_DB_PASSWORD
    API_DB_DATABASE: str = API_DB_DATABASE

    # email
    MAIL_USERNAME: str = MAIL_USERNAME
    MAIL_PASSWORD: str = MAIL_PASSWORD
    MAIL_FROM: str = MAIL_FROM
    MAIL_PORT: str = MAIL_PORT
    MAIL_SERVER: str = MAIL_SERVER
    MAIL_FROM_NAME: str = MAIL_FROM_NAME


settings = Settings()
