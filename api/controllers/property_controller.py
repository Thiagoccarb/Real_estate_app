from typing import List
from fastapi import Depends

from services.auth.auth import AuthService
from services.property.add_property_service import AddPropertyService
from schemas.property_schemas import (
    CreatePropertyRequest,
    CreatePropertyResponse,
    ListPropertyResponse,
    Property,
)
from services.property.list_property_service import ListPropertyService


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

    async def find_all(
        self,
        list_property_service: ListPropertyService = Depends(ListPropertyService),
    ) -> CreatePropertyResponse:
        properties: List[Property] = await list_property_service.execute()
        return ListPropertyResponse(result=properties)
