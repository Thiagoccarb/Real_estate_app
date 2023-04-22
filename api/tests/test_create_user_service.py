# from unittest import IsolatedAsyncioTestCase
# from unittest.mock import MagicMock

# from utils.encoding import PasswordManager
# from services.user.create_user_service import AddUserService
# from schemas.user_schemas import CreateUserRequest, User
# from database.repositories.user_repository import UsersRepository
# from errors.status_error import StatusError


# class TestAddUserService(IsolatedAsyncioTestCase):
#     async def test_execute_with_valid_request_should_return_user(self):
#         request = CreateUserRequest(email="test@example.com", password="Password1")
#         user = User(id=1, email=request.email, password=request.password)

#         user_repository_mock = MagicMock(UsersRepository)
#         user_repository_mock.check_existing_user_by_email.return_value = None
#         user_repository_mock.add.return_value = user

#         pass_manager_mock = MagicMock(PasswordManager)
#         pass_manager_mock.encrypt.return_value = request.password

#         service = AddUserService(user_repository_mock, pass_manager_mock)
#         result = await service.execute(request)

#         self.assertEqual(result, user)
#         user_repository_mock.check_existing_user_by_email.assert_called_once_with(request.email)
#         user_repository_mock.add.assert_called_once_with(request)
#         pass_manager_mock.encrypt.assert_called_once_with(request.password)

#     async def test_execute_with_invalid_email_should_raise_status_error(self):
#         request = CreateUserRequest(email="invalid_email", password="Password1")

#         user_repository_mock = MagicMock(UsersRepository)
#         pass_manager_mock = MagicMock(PasswordManager)

#         service = AddUserService(user_repository_mock, pass_manager_mock)

#         with self.assertRaises(StatusError) as context:
#             await service.execute(request)

#         self.assertEqual(context.exception.status_code, 422)
#         self.assertEqual(context.exception.error_type, "unprocessable_entity")

#     async def test_execute_with_existing_email_should_raise_status_error(self):
#         request = CreateUserRequest(email="existing@example.com", password="Password1")

#         user_repository_mock = MagicMock(UsersRepository)
#         user_repository_mock.check_existing_user_by_email.return_value = User(id=1, email=request.email, password="password")
#         pass_manager_mock = MagicMock(PasswordManager)

#         service = AddUserService(user_repository_mock, pass_manager_mock)

#         with self.assertRaises(StatusError) as context:
#             await service.execute(request)

#         self.assertEqual(context.exception.status_code, 422)
#         self.assertEqual(context.exception.error_type, "unprocessable_entity")

#     async def test_execute_with_invalid_password_should_raise_status_error(self):
#         request = CreateUserRequest(email="test@example.com", password="invalid_password")

#         user_repository_mock = MagicMock(UsersRepository)
#         user_repository_mock.check_existing_user_by_email.return_value = None
#         pass_manager_mock = MagicMock(PasswordManager)

#         service = AddUserService(user_repository_mock, pass_manager_mock)

#         with self.assertRaises(StatusError) as context:
#             await service.execute(request)

#         self.assertEqual(context.exception.status_code, 422)
#         self.assertEqual(context.exception.error_type, "unprocessable_entity")
