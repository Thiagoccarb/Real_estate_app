import unittest
from unittest.mock import MagicMock

from database.repositories.property_repository import PropertiesRepository
from schemas.property_schemas import (
    UpdatePropertyRequest,
    UpdatedProperty,
    CreatePropertyRequest,
)
from services.address.update_address_service import UpdateAddressService
from services.property.update_property_service import UpdatePropertyService
from errors.status_error import StatusError


class TestUpdatePropertyService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.property_repository_mock = MagicMock(spec=PropertiesRepository)
        self.update_address_service_mock = MagicMock(spec=UpdateAddressService)

        self.service = UpdatePropertyService(
            property_repository=self.property_repository_mock,
            update_address_service=self.update_address_service_mock,
        )

    async def test_execute_with_valid_request(self):
        request_data = {
            "name": "new name",
            "action": "rent",
            "type": "apartment",
            "description": "new description",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 500.0,
            "address": {
                "street_name": "new street name",
                "number": 123,
                "cep": "11111-111",
            },
            "city": {"name": "new city name", "state": "SP"},
        }
        request = UpdatePropertyRequest(**request_data)
        property_id = 1

        # mock the repository and service methods
        self.property_repository_mock.find_by_id.return_value = CreatePropertyRequest(
            **{
                "name": "old name",
                "action": "sale",
                "type": "house",
                "description": "old description",
                "bedrooms": 3,
                "bathrooms": 2,
                "price": 1000.0,
                "address_id": 1,
            }
        )
        self.property_repository_mock.update_by_id.return_value = UpdatedProperty(
            **request_data
        )
        self.update_address_service_mock.execute.return_value = {
            "id": 1,
            "street_name": "new street name",
            "number": 123,
            "cep": "11111-111",
            "city": {"id": 1, "name": "new city name", "state": "SP"},
        }

        # call the method and verify the result
        result = await self.service.execute(request, property_id)
        expected = UpdatedProperty(
            **{
                **request_data,
                "address": {
                    "street_name": "new street name",
                    "number": 123,
                    "cep": "11111-111",
                    "city_id": 1,
                },
                "city": {"name": "new city name", "state": "SP"},
            }
        )
        self.assertEqual(result, expected)

        # verify the calls to the repository and service methods
        self.property_repository_mock.find_by_id.assert_called_once_with(property_id)
        self.property_repository_mock.update_by_id.assert_called_once_with(
            id=property_id, data=request
        )
        self.update_address_service_mock.execute.assert_called_once_with(
            existing_property_address_id=1,
            request_data=request.address,
        )
    
    async def test_execute_with_invalid_property_id(self):
        request_data = {
            "name": "new name",
            "action": "rent",
            "type": "apartment",
            "description": "new description",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 500.0,
            "address": {
                "street_name": "new street name",
                "number": 123,
                "cep": "11111-111",
            },
            "city": {"name": "new city name", "state": "SP"},
        }
        request = UpdatePropertyRequest(**request_data)
        property_id = 1

        # mock the repository to return None for find_by_id
        self.property_repository_mock.find_by_id.return_value = None

        # call the method and verify that it raises a StatusError with 404 status
        with self.assertRaises(StatusError) as context:
            await self.service.execute(request, property_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.message, "Property not found")

        # verify the calls to the repository and service methods
        self.property_repository_mock.find_by_id.assert_called_once_with(property_id)
        self.property_repository_mock.update_by_id.assert_not_called()
        self.update_address_service_mock.execute.assert_not_called()


    async def test_execute_with_invalid_address(self):
        request_data = {
            "name": "new name",
            "action": "rent",
            "type": "apartment",
            "description": "new description",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 500.0,
            "address": {
                "street_name": "new street name",
                "number": 123,
                "cep": "11111-111",
            },
            "city": {"name": "new city name", "state": "SP"},
        }
        request = UpdatePropertyRequest(**request_data)
        property_id = 1

        # mock the repository to return a property with an address that cannot be updated
        self.property_repository_mock.find_by_id.return_value = CreatePropertyRequest(
            **{
                "name": "old name",
                "action": "sale",
                "type": "house",
                "description": "old description",
                "bedrooms": 3,
                "bathrooms": 2,
                "price": 1000.0,
                "address_id": 1,
            }
        )
        self.update_address_service_mock.execute.side_effect = StatusError(
            status_code=400, message="Invalid address"
        )

        # call the method and verify that it raises a StatusError with 400 status
        with self.assertRaises(StatusError) as context:
            await self.service.execute(request, property_id)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Invalid address")

        # verify the calls to the repository and service methods
        self.property_repository_mock.find_by_id.assert_called_once_with(property_id)
        self.property_repository_mock.update_by_id.assert_not_called()
        self.update_address_service_mock.execute.assert_called_once_with(
            existing_property_address_id=1,
            request_data=request.address,
        )
    async def test_execute_with_invalid_request(self):
        request_data = {
            "name": "new name",
            "action": "rent",
            "type": "apartment",
            "description": "new description",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 500.0,
            "address": {
                "street_name": "new street name",
                "number": 123,
                "cep": "11111-111",
            },
            "city": {"name": "new city name", "state": "SP"},
        }
        invalid_request_data = request_data.copy()
        invalid_request_data["bedrooms"] = -1  # make bedrooms negative to make the request invalid
        request = UpdatePropertyRequest(**invalid_request_data)
        property_id = 1

        # mock the repository method
        self.property_repository_mock.find_by_id.return_value = CreatePropertyRequest(
            **{
                "name": "old name",
                "action": "sale",
                "type": "house",
                "description": "old description",
                "bedrooms": 3,
                "bathrooms": 2,
                "price": 1000.0,
                "address_id": 1,
            }
        )

        # call the method and verify the exception is raised
        with self.assertRaises(StatusError):
            await self.service.execute(request, property_id)

        # verify the calls to the repository method
        self.property_repository_mock.find_by_id.assert_called_once_with(property_id)
        self.property_repository_mock.update_by_id.assert_not_called()
        self.update_address_service_mock.execute.assert_not_called()
