from typing import Optional
from fastapi import Depends, Header, Query, Request

from errors.status_error import StatusError
from utils.pagination import get_pagination_links
from schemas.base import ListPropertyQueries
from services.property.update_property_service import UpdatePropertyService
from services.auth.auth import AuthService
from services.property.remove_property_service import RemovePropertyService
from services.property.add_property_service import AddPropertyService
from schemas.property_schemas import (
    CreatePropertyRequest,
    CreatePropertyResponse,
    ListPropertyResponse,
    Property,
    RemovePropertyResponse,
    UpdatePropertyRequest,
    UpdatePropertyResponse,
)
from services.property.list_property_service import ListPropertyService


class PropertyController:
    async def add(
        self,
        request: CreatePropertyRequest,
        add_property_service: AddPropertyService = Depends(AddPropertyService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> CreatePropertyResponse:
        await auth_service.execute(authorization, decode=True)
        new_property: Property = await add_property_service.execute(request)
        return CreatePropertyResponse(result=new_property)

    async def find_all(
        self,
        request: Request,
        id: Optional[int] = Query(None),
        type: Optional[str] = Query(None, regex="^(apartment|house)$"),
        action: Optional[str] = Query(None, regex="^(rent|sale)$"),
        sort: Optional[str] = Query(None, regex="^(name|price|bedrooms|bathrooms)$"),
        price: Optional[float] = Query(None),
        bathrooms: Optional[int] = Query(None),
        bedrooms: Optional[int] = Query(None),
        order: Optional[str] = Query("ASC", regex="^(ASC|DESC)$"),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        list_property_service: ListPropertyService = Depends(ListPropertyService),
    ) -> ListPropertyResponse:
        if limit > 50:
            raise StatusError(
                "Query limit must be no greater than 50", 400, "invalid_query-limit"
            )
        queries = ListPropertyQueries(
            id=id, type=type, action=action, sort=sort, offset=offset, limit=limit, price=price, bathrooms=bathrooms, bedrooms=bedrooms, order=order
        )
        properties, count = await list_property_service.execute(queries)
        next_page, previous_page = await get_pagination_links(request, count)
        return ListPropertyResponse(
            result=properties, next_page=next_page, previous_page=previous_page
        )

    async def remove_by_id(
        self,
        id: int = Query(..., gt=0),
        add_property_service: RemovePropertyService = Depends(RemovePropertyService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> RemovePropertyResponse:
        await auth_service.execute(authorization=authorization, decode=True)
        await add_property_service.execute(id)
        return RemovePropertyResponse(
            message=f"property with `id` {id} has been removed"
        )

    async def update_by_id(
        self,
        request: UpdatePropertyRequest,
        id: int = Query(..., gt=0),
        update_property_service: UpdatePropertyService = Depends(UpdatePropertyService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> UpdatePropertyResponse:
        await auth_service.execute(authorization=authorization, decode=True)
        updated_property = await update_property_service.execute(request, id)
        return UpdatePropertyResponse(success=True, result=updated_property)
