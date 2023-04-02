import os
from fastapi import Depends
from dotenv import load_dotenv
import jwt

from services.user.update_user_service import UpdateUserService
from errors.status_error import StatusError
from database.repositories.user_repository import UsersRepository
from database.dtos.users_dto import UpdateUser
from schemas.user_schemas import PasswordResetRequest

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 3

class ResetUserPasswordService:
    def __init__(
        self,
        user_repository: UsersRepository = Depends(UsersRepository),
        update_user_service: UpdateUserService = Depends(UpdateUserService)
      ):  
        self.user_repository = user_repository
        self.update_user_service = update_user_service

    async def execute(self, request: PasswordResetRequest, token: str) -> None:
        try:
            print('data')
            data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            email = data.get("sub")
            existing_user = await self.user_repository.find_by_email(email)
            if not existing_user or (existing_user.email != request.email):
                raise StatusError("invalid_credential", 404, "email_not_found")
            await self.update_user_service.execute(id=existing_user.id, request = UpdateUser(password=request.password))
        except StatusError as e:
            raise StatusError(e.status, e.status_code, e.status)
        except Exception as e:
            raise StatusError("invalid token", 401, "unauthorized_user")
