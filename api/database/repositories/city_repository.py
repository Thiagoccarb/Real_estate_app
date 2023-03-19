from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Union, Dict, List
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dtos.cities_dtos import CreateCity
from schemas.city_schemas import City
from database import mappings
from database import get_db


class AbstractCitiesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateCity) -> City:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, id: int) -> Union[City, None]:
        raise NotImplementedError()


class CitiesRepository(AbstractCitiesRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateCity) -> City:
        city = mappings.City(**data.dict())
        self.session.add(city)
        await self.session.commit()

        await self.session.refresh(city)
        return City.from_orm(city)

    async def find_by_id(self, id: int) -> Union[City, None]:
        async with self.session.begin():
            city = await self.session.execute(
                select(mappings.City).where(mappings.City.id == id)
            )
        city = city.scalar()
        city = City.from_orm(city) if city is not None else None
        return city

    async def find_by(self, queries: Dict[str, str]) -> Union[City, None]:
        async with self.session.begin():
            query =  select(mappings.City)
            for key, value in queries.items():
                query = query.where(getattr(mappings.City,key) == value)
            city = await self.session.execute(query)
        city = city.scalar()
        city = City.from_orm(city) if city is not None else None
        return city
