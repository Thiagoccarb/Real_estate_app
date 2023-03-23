from abc import ABC, abstractmethod
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete

from database.dtos.images_dtos import CreateImage
from schemas.image_schemas import CreatedImageData
from database import mappings
from database import get_db


class AbstractImagesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateImage) -> CreatedImageData:
        raise NotImplementedError()

    @abstractmethod
    async def remove_by_property_id(self, property_id: int) -> None:
        raise NotImplementedError()


class ImagesRepository(AbstractImagesRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateImage) -> CreatedImageData:
        image = mappings.Image(**data.dict())
        self.session.add(image)
        await self.session.commit()

        await self.session.refresh(image)
        return CreatedImageData(**{"id": image.id, "created_at": image.created_at})

    async def remove_by_property_id(self, property_id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(mappings.Image).where(mappings.Image.property_id == property_id)
            )
            await self.session.commit()
