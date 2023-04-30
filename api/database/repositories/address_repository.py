from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Union
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.dtos.addresses_dtos import CreateAddress, UpdateAddress
from schemas.address_schema import Address, UpdateAddressRequest
from database import mappings
from database import get_db


class AbstractAddressesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateAddress) -> Address:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, id: int) -> Union[Address, None]:
        raise NotImplementedError()

    @abstractmethod
    async def remove_by_id(self, id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, id: int, data: UpdateAddress) -> Address:
        raise NotImplementedError()


class AddressesRepository(AbstractAddressesRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add(self, data: CreateAddress) -> Address:
        address = mappings.Address(**data.dict())
        self.session.add(address)
        await self.session.commit()

        await self.session.refresh(address)
        return Address.from_orm(address)

    async def find_by_id(self, id: int) -> Union[Address, None]:
        async with self.session.begin():
            address = await self.session.execute(
                select(mappings.Address).where(mappings.Address.id == id)
            )
            address = address.scalar()
        address = Address.from_orm(address) if address is not None else None
        return address

    async def remove_by_id(self, id: int) -> None:
        async with self.session.begin():
            await self.session.execute(
                delete(mappings.Address).where(mappings.Address.id == id)
            )
            await self.session.commit()

    async def update_by_id(self, id: int, data: UpdateAddress) -> Address:
        property_orm = await self.session.get(mappings.Address, id)

        for field, value in data.dict(exclude_none=True).items():
            setattr(property_orm, field, value)

        await self.session.commit()

        return Address.from_orm(property_orm)
