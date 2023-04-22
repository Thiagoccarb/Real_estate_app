from abc import ABC, abstractmethod
from fastapi import Depends
from typing import List, Tuple, Union
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from schemas.base import ListPropertyQueries
from database.dtos.properties_dtos import CreateProperty, UpdateProperty
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
    async def find_all(self, queries: ListPropertyQueries) -> List[PropertyData]:
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, id: int, data: UpdateProperty) -> Property:
        raise NotImplementedError()

    @abstractmethod
    async def remove_by_id(self, id: int, data: UpdateProperty) -> None:
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

    async def find_all(
        self, queries: ListPropertyQueries
    ) -> Tuple[List[Property], int]:
        async with self.session.begin():
            query = (
                select(
                    mappings.Property.id,
                    mappings.Property.name,
                    mappings.Property.action,
                    mappings.Property.type,
                    mappings.Property.description,
                    mappings.Property.price,
                    mappings.Property.bathrooms,
                    mappings.Property.bedrooms,
                    mappings.Property.created_at,
                    mappings.Property.updated_at,
                    mappings.Address.street_name,
                    mappings.Address.cep,
                    mappings.Address.number,
                    mappings.City.name.label("city_name"),
                    mappings.City.state,
                )
                .select_from(mappings.Property)
                .join(
                    mappings.Address,
                    mappings.Property.address_id == mappings.Address.id,
                )
                .join(mappings.City, mappings.Address.city_id == mappings.City.id)
            )
            for q, v in queries.dict(exclude_none=True).items():
                if q in ("sort", "limit", "offset", "order"):
                    continue
                if q in ("price", "bathrooms", "bedrooms"):
                    column = getattr(mappings.Property, q)
                    query = query.where(column >= v)
                else:
                    column = getattr(mappings.Property, q)
                    query = query.where(column == v)
            if queries.sort:
                sort_column = getattr(mappings.Property, queries.sort)
                if queries.order == "DESC":
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())

            query = query.offset(queries.offset).limit(queries.limit)
            result = await self.session.execute(query)
            properties = []
            for item in result.fetchall():
                property_data = {
                    "id": item.id,
                    "name": item.name,
                    "action": item.action,
                    "type": item.type,
                    "description": item.description,
                    "price": item.price,
                    "bathrooms": item.bathrooms,
                    "bedrooms": item.bedrooms,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at,
                    "address": {
                        "cep": item.cep,
                        "street_name": item.street_name,
                        "number": item.number,
                    },
                    "city": {
                        "name": item.city_name,
                        "state": item.state,
                    },
                }

                # Query for the image URLs
                image_query = select(mappings.Image.url).where(
                    mappings.Image.property_id == item.id
                )
                image_result = await self.session.execute(image_query)
                image_urls = [str(url) for url in image_result.scalars()]

                # Add the image URLs to the property data
                property_data["image_urls"] = image_urls

                properties.append(PropertyData(**property_data))

        count_query = (
            select(func.count())
            .select_from(mappings.Property)
            .join(mappings.Address, mappings.Property.address_id == mappings.Address.id)
            .join(mappings.City, mappings.Address.city_id == mappings.City.id)
        )

        # Apply filters to count query
        for q, v in queries.dict(exclude_none=True).items():
            if q in ("sort", "limit", "offset", "order"):
                continue
            column = getattr(mappings.Property, q)
            count_query = count_query.where(column == v)

        # Execute count query
        async with self.session.begin():
            total_count = await self.session.execute(count_query)
        total_count = total_count.scalar()
        return properties, total_count

    async def remove_by_id(self, id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(mappings.Property).where(mappings.Property.id == id)
            )
            await self.session.commit()

    async def update_by_id(self, id: int, data: UpdateProperty) -> Property:
        property_orm = await self.session.get(mappings.Property, id)

        for field, value in data.dict(exclude_none=True).items():
            setattr(property_orm, field, value)

        await self.session.commit()

        return Property.from_orm(property_orm)
