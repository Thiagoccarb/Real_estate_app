from abc import ABC, abstractmethod
from fastapi import Depends
from typing import List, Union
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from database.dtos.properties_dtos import CreateProperty
from schemas.property_schemas import Property, PropertyData
from database import mappings
from database import get_db


class AbstractPropertiesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateProperty) -> Property:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, id: int) -> Union[Property, None]:
        raise NotImplementedError()

    @abstractmethod
    async def find_all(self) -> List[Property]:
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

    async def find_all(self) -> List[PropertyData]:
        async with self.session.begin():
            subquery = (
                select(func.group_concat(mappings.Image.url))
                .where(mappings.Image.property_id == mappings.Property.id)
                .label("image_urls")
            )
            query = select(
                mappings.Property.id,
                mappings.Property.name,
                mappings.Property.action,
                mappings.Property.type,
                mappings.Property.address_id,
                mappings.Property.created_at,
                mappings.Property.updated_at,
            ).add_columns(subquery)
            result = await self.session.execute(query)

            properties = [
                PropertyData(
                    **{
                        "id": item.id,
                        "name": item.name,
                        "image_urls": [
                            str(url) for url in item.image_urls.split(",") if url
                        ]
                        if item.image_urls
                        else [],
                        "action": item.action,
                        "type": item.type,
                        "address_id": item.address_id,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                    }
                )
                for item in result.fetchall()
            ]

        return properties
