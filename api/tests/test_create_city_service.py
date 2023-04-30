# from fastapi import HTTPException
# from unittest.mock import AsyncMock, Mock
# import pytest
# import imghdr

# from database.dtos.cities_dtos import CreateCity
# from schemas.city_schemas import CreateCityRequest, City
# from database.repositories.city_repository import CitiesRepository
# from services.city.create_city_service import AddCityService
# from errors.status_error import StatusError


# @pytest.fixture()
# def cities_repository():
#     return AsyncMock(spec=CitiesRepository)


# @pytest.fixture()
# def add_city_service(cities_repository):
#     return AddCityService(city_repository=cities_repository)


# @pytest.mark.asyncio
# async def test_add_city_service_returns_new_city(cities_repository, add_city_service):
#     # Arrange
#     request = CreateCityRequest(name="Test City", state="state")
#     cities_repository.add.return_value = City(
#         id=1, name=request.name, state=request.state
#     )

#     # Act
#     response = await add_city_service.execute(request)

#     # Assert
#     assert response.id == 1
#     assert response.name == request.name
