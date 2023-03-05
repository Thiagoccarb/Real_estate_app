from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Union
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dtos.addresses_dtos import CreateAddress
from schemas.address_schema import Address
from database import mappings
from database import get_db


class AbstractAddressesRepository(ABC):
    @abstractmethod
    async def add(self, data: CreateAddress) -> Address:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, id: int) -> Union[Address, None]:
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
