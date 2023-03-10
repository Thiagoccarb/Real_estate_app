import os
from fastapi import Header
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from errors.status_error import StatusError

from schemas.auth_schemas import UserCredentialsRequest


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day = 24 * 60 minutes


class AuthService:
    def __init__(self):
        self.oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
            tokenUrl="login"
        )
        self.user = {
            "username": "user1",
            "password": "password1",
            "full_name": "User One",
            "email": "user1@example.com",
        }

    def _create_access_token(self, user_id: str):
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = datetime.utcnow() + expires_delta

        payload = {
            "sub": user_id,
            "exp": expires_at,
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=["HS256"])
        return access_token

    def validate_token(self, authorization: str = Header(None)):
        if not authorization:
            raise StatusError("unauthorized access", 401, "unauthorized_user")
        try:
            jwt.decode(authorization, SECRET_KEY, algorithms="HS256")
        except Exception:
            raise StatusError("invalid token", 401, "unauthorized_user")

    def execute(self, request: UserCredentialsRequest):
        if (
            self.user.get("username") == request.username
            and self.user.get("password") == request.password
        ):
            token = self._create_access_token("test")
            return token
        raise StatusError("invalid user credentials", 401, "unauthorized_user")
