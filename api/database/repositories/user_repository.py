from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Union
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dtos.users_dto import CreateUser, UpdateUser
from schemas.user_schemas import User
from database import mappings
from database import get_db


class AbstractUsersRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateUser) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def check_existing_user_by_email(self, email: str) -> bool:
        raise NotImplementedError()


class UsersRepository(AbstractUsersRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateUser) -> User:
        user = mappings.User(**data.dict())
        self.session.add(user)
        await self.session.commit()

        await self.session.refresh(user)
        return User.from_orm(user)

    async def check_existing_user_by_email(self, email: str) -> Union[User, None]:
        async with self.session.begin():
            user = await self.session.execute(
                select(mappings.User).where(mappings.User.email == email)
            )
        user = user.scalar()
        return user if user else None

    async def find_by_email(self, email: str) -> Union[User, None]:
        async with self.session.begin():
            user = await self.session.execute(
                select(mappings.User).where(mappings.User.email == email)
            )
            user = user.scalar()
        return User.from_orm(user) if user else None

    async def find_by_id(self, id: int) -> Union[User, None]:
        async with self.session.begin():
            user = await self.session.execute(
                select(mappings.User).where(mappings.User.id == id)
            )
        user = user.scalar()
        return user if user else None

    async def update_by_id(self, id: int, data: UpdateUser) -> User:
        user_orm = await self.session.get(mappings.User, id)

        for field, value in data.dict(exclude_none=True).items():
            setattr(user_orm, field, value)

        await self.session.commit()

        return User.from_orm(user_orm)
