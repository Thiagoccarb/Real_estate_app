from fastapi import Depends
import re

from database.mappings import City
from database.dtos.addresses_dtos import CreateAddress
from database.dtos.cities_dtos import CreateCity
from schemas.address_schema import CreateAddressRequest, Address
from database.repositories.city_repository import CitiesRepository
from database.repositories.address_repository import AddressesRepository
from errors.status_error import StatusError


class AddAddressService:
    def __init__(
        self,
        address_repository: AddressesRepository = Depends(AddressesRepository),
        city_repository: CitiesRepository = Depends(CitiesRepository),
    ):
        self.address_repository = address_repository
        self.city_repository = city_repository

    async def execute(self, request: CreateAddressRequest) -> Address:
        city: City = await self.city_repository.find_by(
            {"name": request.city_data.name, "state": request.city_data.state}
        )
        if not city:
            city = await self.city_repository.add(
                CreateCity(name=request.city_data.name, state=request.city_data.state)
            )
        pattern = r"^\d{8}|\d{5}-\d{3}$"
        if not re.match(pattern, request.cep):
            raise StatusError(
                "cep must be in the format XXXXX-XXX or XXXXXXXX",
                422,
                "unprocessable_entity",
            )
        new_address = await self.address_repository.add(
            CreateAddress(
                street_name=request.street_name,
                city_id=city.id,
                number=request.number,
                cep=request.cep,
            )
        )
        return new_address
