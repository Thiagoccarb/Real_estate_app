# import os
# import unittest
# from unittest.mock import patch, MagicMock
# from asynctest import CoroutineMock
# from dotenv import load_dotenv
# from config.settings import settings
# from database.repositories.user_repository import UsersRepository
# from schemas.user_schemas import EmailRequest
# from services.user.send_user_email_service import SendUserEmailService
# from utils.send_email import send_email_background

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")

# class TestSendUserEmailService(unittest.IsolatedAsyncioTestCase):
#     async def setUp(self):
#         self.mock_user_repository = UsersRepository()
#         self.send_user_email_service = SendUserEmailService(user_repository=self.mock_user_repository)

#     async def test_execute(self):
#         request = EmailRequest(email="test@example.com")
#         expected_token = "valid_token"
#         expected_url = f"{settings.BASE_URL}/users/reset-password?token={expected_token}"
#         background_tasks_mock = MagicMock()

#         with patch("jwt.encode") as mock_encode:
#             mock_encode.return_value = expected_token
#             with patch.object(send_email_background, "delay") as mock_delay:
#                 mock_delay.return_value = CoroutineMock()
#                 await self.send_user_email_service.execute(request=request, background_tasks=background_tasks_mock)
#                 mock_encode.assert_called_once_with({"sub": request.email, "exp": mock_encode}, SECRET_KEY, algorithm="HS256")
#                 mock_delay.assert_called_once_with(
#                     background_tasks_mock,
#                     'No reply',
#                     request.email,
#                     {
#                         "url": expected_url,
#                     },
#                 )
