from typing import List, Tuple
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from schemas.base import ListPropertyQueries
from schemas.property_schemas import Property
from services.property.list_property_service import ListPropertyService
from database.repositories.property_repository import PropertiesRepository


class TestListPropertyService(IsolatedAsyncioTestCase):
    async def test_execute_with_valid_queries(self):
        # Arrange
        queries = ListPropertyQueries(limit=10, offset=0)
        properties = [Property(id=1, name="Test Property 1", bedrooms=1, bathrooms=1, description="test"), Property(id=2, name="Test Property 2",bedrooms=1, bathrooms=1, description="test")]
        count = 2

        property_repository_mock = MagicMock(spec=PropertiesRepository)
        property_repository_mock.find_all.return_value = (properties, count)

        service = ListPropertyService(property_repository=property_repository_mock)

        # Act
        result = await service.execute(queries)

        # Assert
        property_repository_mock.find_all.assert_called_once_with(queries)
        self.assertEqual(result, (properties, count))
