from fastapi import Depends
import re

from utils.encoding import PasswordManager
from schemas.user_schemas import UpdateUserRequest, User
from database.repositories.user_repository import UsersRepository
from errors.status_error import StatusError


class UpdateUserService:
    def __init__(
        self,
        user_repository: UsersRepository = Depends(UsersRepository),
        pass_manager: PasswordManager = Depends(PasswordManager),
    ):
        self.user_repository = user_repository
        self.pass_manager = pass_manager

    async def execute(self, id, request: UpdateUserRequest) -> User:
        if request.email:
            if not re.match(
                r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.(com|com\.br|net)$", request.email
            ):
                raise StatusError(
                    "field `email` must be like user@gmail.com (e.g:userEmail123@gmail.com, us123Et@yahoo.com.br, us123Et@yahoo.com.br)",
                    422,
                    "unprocessable_entity",
                )

            existing_user = await self.user_repository.check_existing_user_by_email(
                request.email
            )

            if existing_user is not None:
                raise StatusError(
                    "field `email` must be unique, please choose modify {email}",
                    422,
                    "unprocessable_entity",
                    email=request.email,
                )
        if request.password:
            if not re.match(
                r"^(?!.*(\w)\1\1\1)[A-Za-z\d@$!%*?&]{7,}(?=.*[A-Z])(?=.*[@$!%*?&]).*$",
                request.password,
            ):
                raise StatusError(
                    """
                    field `password` must match the following pattern:
                    1 - greater or equal than seven characters
                    2 - at least one capital letter and one special character
                    3 - no more than three equal consecutive character
                    """,
                    422,
                    "unprocessable_entity",
                )
            hash_password = self.pass_manager.encrypt(request.password)
            request.password = hash_password
        new_user = await self.user_repository.update_by_id(id, request)
        return new_user
