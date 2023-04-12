from fastapi import Depends

from schemas.address_schema import UpdateAddressRequest, UpdateAddressResponse
from services.address.update_address_service import UpdateAddressService
from schemas.property_schemas import Property, UpdatePropertyRequest, UpdatedProperty
from database.dtos.cities_dtos import UpdateCity
from database.dtos.addresses_dtos import UpdateAddress
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError


class UpdatePropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        update_address_service: UpdateAddressService = Depends(UpdateAddressService),
    ):
        self.property_repository = property_repository
        self.update_address_service = update_address_service

    async def execute(self, request: UpdatePropertyRequest, id) -> UpdatedProperty:
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
        existing_property: Property = await self.property_repository.find_by_id(id)
        if not existing_property:
            raise StatusError(
                "property with `id` {id} not found", 404, "not_found", id=id
            )

        request_data = request.dict()
        if request.address:
            request_data.update(request.address.dict(exclude_none=True))
        if request.city:
            request_data.update(request.city.dict(exclude_none=True))

        update_data = {
            "street_name": request_data.get("street_name"),
            "number": request_data.get("number"),
            "cep": request_data.get("cep"),
            "city": {
                "name": request_data["city"].get("name"),
                "state": request_data["city"].get("state"),
            },
        }
        updated_address: UpdateAddressResponse = (
            await self.update_address_service.execute(
                existing_property.address_id, UpdateAddressRequest(**update_data)
            )
        )
        updated_property: Property = await self.property_repository.update_by_id(
            id=id, data=request
        )

        return UpdatedProperty(
            name=updated_property.name,
            action=updated_property.action,
            type=updated_property.type,
            price=updated_property.price,
            description=request.description,
            bedrooms=request.bedrooms,
            bathrooms=request.bathrooms,
            address=UpdateAddress(
                street_name=updated_address.street_name,
                number=updated_address.number,
                cep=updated_address.cep,
                city_id=updated_address.city_id,
            ),
            city=UpdateCity(
                name=updated_address.city.name, state=updated_address.city.state
            ),
        )
