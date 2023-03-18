import os
import re
from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from schemas.user_schemas import User
from utils.encoding import PasswordManager
from database.repositories.user_repository import UsersRepository
from errors.status_error import StatusError

from schemas.auth_schemas import UserCredentialsRequest


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day = 24 * 60 minutes


class AuthService:
    def __init__(
        self,
        user_repository: UsersRepository = Depends(UsersRepository),
        pass_manager: PasswordManager = Depends(PasswordManager),
    ):
        self.oauth2_scheme: OAuth2PasswordBearer = (
            OAuth2PasswordBearer(tokenUrl="login"),
        )
        self.user_repository = user_repository
        self.pass_manager = pass_manager

    async def _create_access_token(self, email: str, password: str):
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = datetime.utcnow() + expires_delta
        existing_user: User = await self.user_repository.find_by_email(email)
        if not existing_user or not self.pass_manager.verify(
            password, existing_user.password.encode()
        ):
            raise StatusError("invalid credentials", 401, "invalid_credentials")
        payload = {
            "sub": existing_user.id,
            "exp": expires_at,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return access_token

    async def _decode_token(self, authorization: Optional[str]):
        if not authorization:
            raise StatusError("unauthorized access", 401, "unauthorized_user")
        try:
            data = jwt.decode(authorization, SECRET_KEY, algorithms="HS256")
            existing_user: User = await self.user_repository.find_by_id(data.get("sub"))
            if not existing_user:
                raise StatusError("invalid token", 401, "user_data_not_fount")
            return existing_user.id
        except Exception:
            raise StatusError("invalid token", 401, "unauthorized_user")

    async def execute(
        self,authorization: Optional[str], request: Optional[UserCredentialsRequest] = None, decode: bool = True
    ):
        if decode:
            return await self._decode_token(authorization)
        return await self._create_access_token(request.email, request.password)
