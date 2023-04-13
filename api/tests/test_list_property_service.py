import pytest
from typing import List, Tuple
from unittest.mock import Mock

from schemas.base import ListPropertyQueries
from schemas.property_schemas import Property
from database.repositories.property_repository import PropertiesRepository
from services.property.list_property_service import ListPropertyService

@pytest.fixture
def fake_property_repository():
    class FakePropertyRepository(PropertiesRepository):
        async def find_all(self, queries: ListPropertyQueries) -> Tuple[List[Property], int]:
            properties = [
                Property(
                    id=1,
                    name="Property 1",
                    action="rent",
                    type="apartment",
                    description="This is a nice apartment",
                    price=1000.0,
                    bathrooms=2,
                    bedrooms=3,
                    address_id=1,
                    created_at="2022-04-11T22:28:20.532",
                    updated_at="2022-04-11T22:28:20.532",
                    street_name="Test Street",
                    cep="12345-678",
                    number="123",
                    city_name="Test City",
                    state="TS",
                ),
                Property(
                    id=2,
                    name="Property 2",
                    action="rent",
                    type="apartment",
                    description="This is another nice apartment",
                    price=1500.0,
                    bathrooms=3,
                    bedrooms=4,
                    address_id=2,
                    created_at="2022-04-11T22:28:20.532",
                    updated_at="2022-04-11T22:28:20.532",
                    street_name="Test Street",
                    cep="12345-678",
                    number="456",
                    city_name="Test City",
                    state="TS",
                ),
            ]
            return properties, len(properties)
    return FakePropertyRepository()

@pytest.fixture
def list_property_service(fake_property_repository):
    return ListPropertyService(property_repository=fake_property_repository)

@pytest.mark.asyncio
async def test_list_all_properties(list_property_service):
    queries = ListPropertyQueries()
    properties, count = await list_property_service.execute(queries)

    assert len(properties) == 2
    assert count == 2
