from typing import Optional
from fastapi import Depends, Query, Request

from errors.status_error import StatusError
from utils.pagination import get_pagination_links
from schemas.base import ListPropertyQueries
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
        request: Request,
        id: Optional[int] = Query(None),
        type: Optional[str] = Query(None, regex="^(apartment|house)$"),
        action: Optional[str] = Query(None, regex="^(rent|sale)$"),
        sort: Optional[str] = Query(None, regex="^(name)$"),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        list_property_service: ListPropertyService = Depends(ListPropertyService),
    ) -> ListPropertyResponse:
        if limit > 50:
            raise StatusError(
                "Query limit must be no greater than 50", 400, "invalid_query-limit"
            )
        queries = ListPropertyQueries(
            id=id, type=type, action=action, sort=sort, offset=offset, limit=limit
        )
        properties, count = await list_property_service.execute(queries)
        next_page, previous_page = await get_pagination_links(request, count)
        return ListPropertyResponse(
            result=properties, next_page=next_page, previous_page=previous_page
        )
