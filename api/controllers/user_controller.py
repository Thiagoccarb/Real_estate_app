from fastapi import Depends

from services.user.create_user_service import AddUserService
from schemas.user_schemas import (
    CreateUserRequest,
    CreateUserResponse,
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
