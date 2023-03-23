from fastapi import Depends
import re

from schemas.city_schemas import City
from database.dtos.addresses_dtos import UpdateAddress
from database.dtos.cities_dtos import CreateCity, UpdateCity
from schemas.address_schema import Address, UpdateAddressRequest, UpdateAddressResponse
from database.repositories.city_repository import CitiesRepository
from database.repositories.address_repository import AddressesRepository
from errors.status_error import StatusError


class UpdateAddressService:
    def __init__(
        self,
        address_repository: AddressesRepository = Depends(AddressesRepository),
        city_repository: CitiesRepository = Depends(CitiesRepository),
    ):
        self.address_repository = address_repository
        self.city_repository = city_repository

    async def execute(
        self, id: int, request: UpdateAddressRequest
    ) -> UpdateAddressResponse:
        if request.cep:
            pattern = r"^\d{5}(-\d{3})?$"
            match = re.match(pattern, request.cep)
            if not match:
                raise StatusError(
                    "cep must be in the format XXXXX-XXX or XXXXXXXX",
                    422,
                    "unprocessable_entity",
                )
        city_request = request.city.dict()
        city_name = city_request.get("name", None)
        city_state = city_request.get("state", None)

        if city_name and city_state:
            city: City = await self.city_repository.find_by(
                {"name": request.city.name, "state": request.city.state}
            )
            if not city:
                city: City = await self.city_repository.add(
                    CreateCity(name=request.city.name, state=request.city.state)
                )
        else:
            address_data: Address = await self.address_repository.find_by_id(id)
            city: City = await self.city_repository.find_by_id(address_data.city_id)
        updated_address: Address = await self.address_repository.update_by_id(
            id,
            UpdateAddress(
                street_name=request.street_name,
                city_id=city.id,
                number=request.number,
                cep=request.cep,
            ),
        )
        return UpdateAddressResponse(
            street_name=updated_address.street_name,
            number=updated_address.number,
            cep=updated_address.cep,
            city_id=city.id,
            city=UpdateCity(
                name=city_name or city.name,
                state=city_state or city.state,
            ),
        )
