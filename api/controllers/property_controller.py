from fastapi import Depends

from services.auth.auth import AuthService
from services.property.add_property_service import AddPropertyService
from schemas.property_schemas import (
    CreatePropertyRequest,
    CreatePropertyResponse,
    Property,
)


class PropertyController:
    async def add(
        self,
        request: CreatePropertyRequest,
        add_property_service: AddPropertyService = Depends(AddPropertyService),
        auth_service: AuthService = Depends(AuthService),
    ) -> CreatePropertyResponse:
        await auth_service.execute(decode=True)
        new_property: Property = await add_property_service.execute(request)
        return CreatePropertyResponse(result=new_property)
