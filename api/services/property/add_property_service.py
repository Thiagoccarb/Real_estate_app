from fastapi import Depends

from schemas.address_schema import CreateAddressRequest
from schemas.property_schemas import CreatePropertyRequest, Property
from services.address.create_address_service import AddAddressService
from database.dtos.properties_dtos import CreateProperty
from database.repositories.property_repository import PropertiesRepository
from database.dtos.cities_dtos import CreateCity
from errors.status_error import StatusError


class AddPropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        add_address_service: AddAddressService = Depends(AddAddressService),
    ):
        self.property_repository = property_repository
        self.add_address_service = add_address_service

    async def execute(self, request: CreatePropertyRequest) -> Property:
        if request.type not in ("apartment", "house"):
            raise StatusError(
                'field `type` must be "apartment" or "house"',
                422,
                "unprocessable_entity",
            )

        if request.action not in ("rent", "sale"):
            raise StatusError(
                'field `action` must be "rent" or "sale"', 422, "unprocessable_entity"
            )

        new_address = await self.add_address_service.execute(
            CreateAddressRequest(
                street_name=request.address.street_name,
                number=request.address.number,
                cep=request.address.cep,
                city_data=CreateCity(name=request.city.name, state=request.city.state),
            )
        )

        new_property = await self.property_repository.add(
            data=CreateProperty(
                name=request.name,
                action=request.action,
                type=request.type,
                address_id=new_address.id,
            )
        )
        return new_property
