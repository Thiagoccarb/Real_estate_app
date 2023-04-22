from fastapi import Depends

from schemas.auth_schemas import UserCredentialsRequest, UserCredentialsResponse
from services.auth.auth import AuthService


class AuthController:
    async def login(
        self,
        request: UserCredentialsRequest,
        login_service: AuthService = Depends(AuthService),
    ) -> str:
        token = await login_service.execute(request=request, decode=False)
        return UserCredentialsResponse(result={"token": token})
