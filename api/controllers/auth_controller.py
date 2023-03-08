from fastapi import Depends

from schemas.auth_schemas import UserCredentialsRequest, UserCredentialsResponse
from services.auth.auth import AuthService


class AuthController:
    def login(
        self,
        request: UserCredentialsRequest,
        login_service: AuthService = Depends(AuthService),
    ) -> str:

        token = login_service.execute(request)
        return UserCredentialsResponse(result={"token": token})
