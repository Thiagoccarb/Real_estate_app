from fastapi import BackgroundTasks, Depends
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from errors.status_error import StatusError
from database.repositories.user_repository import UsersRepository
from schemas.user_schemas import EmailRequest
from utils.send_email import send_email_background

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 3  

class SendUserEmailService:
    def __init__(
        self,
        user_repository: UsersRepository = Depends(UsersRepository),
    ):
        self.user_repository = user_repository

      
    async def execute(self, request: EmailRequest, background_tasks: BackgroundTasks) -> None:
        # existing_user = await self.user_repository.find_by_email(request.email)
        # if not existing_user:
        #     raise StatusError("email_not_found", 404, "the provided email was not found.")
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = datetime.utcnow() + expires_delta
        payload = {
            "sub": request.email,
            "exp": expires_at,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        send_email_background(
            background_tasks,
            'No reply',   
            request.email, 
            {
                "url": f"{BASE_URL}/users/reset-password?token={token}",
            },
          )
        print('email successfully sent')