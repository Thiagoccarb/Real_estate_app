# import re
# from unittest import IsolatedAsyncioTestCase
# from unittest.mock import patch
# from asynctest import CoroutineMock

# from fastapi import HTTPException
# from services.user.update_user_service import UpdateUserService
# from database.repositories.user_repository import UsersRepository
# from schemas.user_schemas import UpdateUserRequest, User
# from utils.encoding import PasswordManager


# class TestUpdateUserService(IsolatedAsyncioTestCase):
#     async def asyncSetUp(self):
#         self.user_repository = UsersRepository()
#         self.password_manager = PasswordManager()
#         self.service = UpdateUserService(
#             user_repository=self.user_repository,
#             pass_manager=self.password_manager,
#         )

#     async def test_update_user_with_valid_request(self):
#         user = User(
#             id=1,
#             name="John Doe",
#             email="john@example.com",
#             password="password123",
#             is_active=True,
#         )

#         request = UpdateUserRequest(name="Jane Doe")

#         with patch.object(self.user_repository, "update_by_id", new=CoroutineMock(return_value=user)):
#             updated_user = await self.service.execute(1, request)

#         self.assertEqual(updated_user.name, request.name)

#     async def test_update_user_with_invalid_email(self):
#         request = UpdateUserRequest(email="not_an_email")

#         with self.assertRaises(HTTPException) as cm:
#             await self.service.execute(1, request)

#         self.assertEqual(cm.exception.status_code, 422)
#         self.assertEqual(cm.exception.detail, "field `email` must be like user@gmail.com (e.g:userEmail123@gmail.com, us123Et@yahoo.com.br, us123Et@yahoo.com.br)")

#     async def test_update_user_with_existing_email(self):
#         user = User(
#             id=1,
#             name="John Doe",
#             email="john@example.com",
#             password="password123",
#             is_active=True,
#         )

#         request = UpdateUserRequest(email="john@example.com")

#         with patch.object(self.user_repository, "check_existing_user_by_email", new=CoroutineMock(return_value=user)):
#             with self.assertRaises(HTTPException) as cm:
#                 await self.service.execute(1, request)

#         self.assertEqual(cm.exception.status_code, 422)
#         self.assertEqual(cm.exception.detail, "field `email` must be unique, please choose modify john@example.com")

#     async def test_update_user_with_invalid_password(self):
#         request = UpdateUserRequest(password="weak")

#         with self.assertRaises(HTTPException) as cm:
#             await self.service.execute(1, request)

#         self.assertEqual(cm.exception.status_code, 422)
#         self.assertEqual(cm.exception.detail, "field `password` must match the following pattern:\n                    1 - greater or equal than seven characters\n                    2 - at least one capital letter and one special character\n                    3 - no more than three equal consecutive character")

#     async def test_update_user_with_valid_password(self):
#         user = User(
#             id=1,
#             name="John Doe",
#             email="john@example.com",
#             password="password123",
#             is_active=True,
#         )

#         request = UpdateUserRequest(password="StrongPassword!1")

#         with patch.object(self.user_repository, "update_by_id", new=CoroutineMock(return_value=user)):
#             updated_user = await self.service.execute(1, request)

#         self.assertTrue(re.match(r"^(?!.*(\w)\1\1\1)[A-Za-z\d@$!%*?&]{7,}(?=.*[A-Z])(?=.*[@$!%*?&]).*$", updated_user.password))
