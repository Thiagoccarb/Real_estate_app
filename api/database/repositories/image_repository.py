from abc import ABC, abstractmethod
from typing import List, Union
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select

from database.dtos.images_dtos import CreateImage
from schemas.image_schemas import CreatedImageData, Image
from database import mappings
from database import get_db


class AbstractImagesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateImage) -> CreatedImageData:
        raise NotImplementedError()

    @abstractmethod
    async def remove_by_property_id(self, property_id: int) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def find_all_by_property_id(self, property_id: int) -> Union[Image, None]:
        raise NotImplementedError()

class ImagesRepository(AbstractImagesRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateImage) -> Image:
        image = mappings.Image(**data.dict())
        self.session.add(image)
        await self.session.commit()

        await self.session.refresh(image)
        return Image.from_orm(image)
    
    async def find_all_by_property_id(self, property_id: int) -> List[Image]:
        async with self.session.begin():
            image = await self.session.execute(
                select(mappings.Image).where(mappings.Image.property_id == property_id)
            )
        image = image.scalars().all()
        image = [Image.from_orm(item) for item in image] if image else None
        return image

    async def remove_by_property_id(self, property_id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(mappings.Image).where(mappings.Image.property_id == property_id)
            )
            await self.session.commit()

    async def find_by_audio_hash(self, audio_hash: str) -> Union[Image, None]:
        async with self.session.begin():
            image = await self.session.execute(
                select(mappings.Image).where(mappings.Image.audio_hash == audio_hash)
            )
        image = image.scalar()
        image = Image.from_orm(image) if image is not None else None
        return image

    async def update_position(self, image_id: int, position: int) -> None:
        async with self.session.begin():
            image = await self.session.get(mappings.Image, image_id)
            if image is not None:
                image.position = position
                await self.session.commit()
