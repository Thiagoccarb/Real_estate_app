from fastapi import BackgroundTasks, Depends, Query

from services.user.reset_user_password_service import ResetUserPasswordService
from services.user.send_user_email_service import SendUserEmailService
from services.user.create_user_service import AddUserService
from schemas.base import BaseResponse
from schemas.user_schemas import (
    CreateUserRequest,
    CreateUserResponse,
    EmailRequest,
    PasswordResetRequest,
    User,
)


class UserController:
    async def add(
        self,
        request: CreateUserRequest,
        add_user_service: AddUserService = Depends(AddUserService),
    ) -> CreateUserResponse:
        new_user: User = await add_user_service.execute(request)
        return CreateUserResponse(result=new_user)

    async def send_email(
        self,
        request: EmailRequest,
        background_tasks: BackgroundTasks,
        send_user_email_service: SendUserEmailService = Depends(SendUserEmailService),
    ) -> None:
        await send_user_email_service.execute(request, background_tasks)
        return BaseResponse(success=True, message="Please, check your email.")
    
    async def reset_password(
        self,
        request: PasswordResetRequest,
        token = Query(...),
        reset_password_service: ResetUserPasswordService = Depends(ResetUserPasswordService),
    ) -> None:
        await reset_password_service.execute(request, token)
        return BaseResponse(success=True, message="user password has been successfully changed.")
