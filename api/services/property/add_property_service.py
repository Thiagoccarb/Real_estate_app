from fastapi import Depends

from schemas.address_schema import CreateAddressRequest
from schemas.property_schemas import CreatePropertyRequest, CreatedProperty, Property
from services.address.create_address_service import AddAddressService
from database.dtos.addresses_dtos import AddressWithCity, AddressWithoutId
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

        new_address_data: AddressWithCity = await self.add_address_service.execute(
            CreateAddressRequest(
                street_name=request.address.street_name,
                number=request.address.number,
                cep=request.address.cep,
                city_data=CreateCity(name=request.city.name, state=request.city.state),
            )
        )
        new_property: Property = await self.property_repository.add(
            data=CreateProperty(
                name=request.name,
                action=request.action,
                type=request.type,
                address_id=new_address_data.id,
                price=request.price,
                description=request.description,
                bedrooms=request.bedrooms,
                bathrooms=request.bathrooms,
            )
        )
        return CreatedProperty(
            id=new_property.id,
            name=new_property.name,
            action=new_property.action,
            type=new_property.type,
            price=new_property.price,
            description=new_property.description,
            bedrooms=new_property.bedrooms,
            bathrooms=new_property.bathrooms,
            address=AddressWithoutId(
                street_name=new_address_data.street_name,
                number=new_address_data.number,
                cep=new_address_data.cep,
            ),
            city=CreateCity(
                name=new_address_data.city.name, state=new_address_data.city.state
            ),
        )
