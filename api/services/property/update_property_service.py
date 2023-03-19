from fastapi import Depends

from schemas.property_schemas import Property, UpdatePropertyRequest
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError


class UpdatePropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
    ):
        self.property_repository = property_repository

    async def execute(self, request: UpdatePropertyRequest, id) -> Property:
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

        updated_property = await self.property_repository.update_by_id(
            id=id, data=request
        )
        return updated_property
