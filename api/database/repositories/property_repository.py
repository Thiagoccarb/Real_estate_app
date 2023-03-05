from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Union
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dtos.properties_dtos import CreateProperty
from schemas.property_schemas import Property
from database import mappings
from database import get_db


class AbstractPropertiesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateProperty) -> Property:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, id: int) -> Union[Property, None]:
        raise NotImplementedError()


class PropertiesRepository(AbstractPropertiesRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateProperty) -> Property:
        property = mappings.Property(**data.dict())
        self.session.add(property)
        await self.session.commit()

        await self.session.refresh(property)
        return Property.from_orm(property)

    async def find_by_id(self, id: int) -> Union[Property, None]:
        async with self.session.begin():
            property = await self.session.execute(
                select(mappings.Property).where(mappings.Property.id == id)
            )
        property = property.scalar()
        property = Property.from_orm(property) if property is not None else None
        return property
