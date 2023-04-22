# from datetime import datetime
# import pytest
# from unittest.mock import MagicMock, patch

# from fastapi import HTTPException

# from database.dtos.users_dto import UpdateUser
# from services.user.reset_user_password_service import ResetUserPasswordService
# from database.repositories.user_repository import UsersRepository
# from services.user.update_user_service import UpdateUserService
# from schemas.user_schemas import PasswordResetRequest, User

# pytestmark = pytest.mark.asyncio

# class TestResetUserPasswordService:

#     async def test_execute_success(self):
#         user_repository_mock = MagicMock(spec=UsersRepository)
#         update_user_service_mock = MagicMock(spec=UpdateUserService)
        
#         service = ResetUserPasswordService(user_repository_mock, update_user_service_mock)

#         request = PasswordResetRequest(
#             email="test@test.com",
#             password="TestPass1",
#         )
#         token = "fake_token"

#         user = User(
#             id=1,
#             email="test@test.com",
#             password="hashed_password",
#             created_at=datetime.now(),
#             updated_at=datetime.now(),
#         )

#         # mock `find_by_email` method to return the user with the given email
#         user_repository_mock.find_by_email.return_value = user

#         # mock `execute` method of `update_user_service` to do nothing and return None
#         update_user_service_mock.execute.return_value = None

#         # call the `execute` method of the service with the given request and token
#         await service.execute(request, token)

#         # check if `find_by_email` method was called once with the given email
#         user_repository_mock.find_by_email.assert_called_once_with(request.email)

#         # check if `execute` method of `update_user_service` was called once with the given user id and password
#         update_user_service_mock.execute.assert_called_once_with(id=user.id, request=UpdateUser(password=request.password))

#     async def test_execute_invalid_token(self):
#         user_repository_mock = MagicMock(spec=UsersRepository)
#         update_user_service_mock = MagicMock(spec=UpdateUserService)
        
#         service = ResetUserPasswordService(user_repository_mock, update_user_service_mock)

#         request = PasswordResetRequest(
#             email="test@test.com",
#             password="TestPass1",
#         )
#         token = "invalid_token"

#         # mock `decode` function from `jwt` module to raise an exception
#         with patch("jwt.decode", side_effect=Exception("Invalid token")):
#             with pytest.raises(HTTPException) as exc_info:
#                 # call the `execute` method of the service with the given request and token
#                 await service.execute(request, token)

#         # check if an HTTPException with the given status, status code and detail was raised
#         assert exc_info.value.status == "invalid token"
#         assert exc_info.value.status_code == 401
#         assert exc_info.value.detail == "unauthorized_user"

#     async def test_execute_invalid_credential(self):
#         user_repository_mock = MagicMock(spec=UsersRepository)
#         update_user_service_mock = MagicMock(spec=UpdateUserService)
        
#         service = ResetUserPasswordService(user_repository_mock, update_user_service_mock)

#         request = PasswordResetRequest(
#             email="test2@test.com",
#             password="TestPass1",
#         )
#         token = "fake_token"

#         # mock `find_by_email` method to return None
#         user_repository_mock.find_by_email.return_value = None

#         with pytest.raises(HTTPException) as exc_info:
#             # call the `execute` method of the service with the given request and token
#             await service.execute(request, token)

#         # check if an HTTPException with the given status, status code and detail was raised
#         assert exc_info.value.status == "invalid_credential"
#         assert exc_info.value.status_code == 404
#         assert exc_info.value
