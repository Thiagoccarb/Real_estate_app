import unittest
from asynctest import CoroutineMock

from schemas.property_schemas import (
    Property,
    UpdatePropertyRequest,
    UpdatedProperty,
    CreatePropertyRequest,
)
from schemas.address_schema import UpdateAddressRequest, UpdateAddressResponse
from database.repositories.property_repository import PropertiesRepository
from services.address.update_address_service import UpdateAddressService
from services.property.update_property_service import UpdatePropertyService
from errors.status_error import StatusError


class TestUpdatePropertyService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.property_repository_mock = CoroutineMock()
        self.update_address_service_mock = CoroutineMock()

        self.service = UpdatePropertyService(
            property_repository=self.property_repository_mock,
            update_address_service=self.update_address_service_mock,
        )

    async def test_execute_with_valid_request(self):
        mock_request_data = {
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
        mock_request = UpdatePropertyRequest(**mock_request_data)
        mock_property_id = 1

        # mock the repository and service methods
        mock_property = CoroutineMock()
        mock_property.id = 1
        mock_property.address_id = 1
        mock_property.name = "test"
        mock_property.price = 100
        mock_property.type = "apartment"
        mock_property.action = "rent"

        self.property_repository_mock.find_by_id = CoroutineMock()
        self.property_repository_mock.find_by_id.return_value = mock_property

        mock_updated_address = UpdateAddressResponse(
            **{
                "street_name": "street_name",
                "cep": "11111-111",
                "city_id": 1,
                "city": {
                    "name": mock_request_data["city"].get("name"),
                    "state": mock_request_data["city"].get("state"),
                },
            }
        )

        self.update_address_service_mock.execute = CoroutineMock()
        self.update_address_service_mock.execute.return_value = mock_updated_address

        self.property_repository_mock.update_by_id = CoroutineMock()
        self.property_repository_mock.update_by_id.return_value = mock_property

        mock_data = mock_request.dict()
        if mock_request.address:
            mock_data.update(mock_request.address.dict(exclude_none=True))
        if mock_request.city:
            mock_data.update(mock_request.city.dict(exclude_none=True))

        mock_update_data = {
            "street_name": mock_data.get("street_name"),
            "number": mock_data.get("number"),
            "cep": mock_data.get("cep"),
            "city": {
                "name": mock_data["city"].get("name"),
                "state": mock_data["city"].get("state"),
            },
        }
        # call the method and verify the result
        await self.service.execute(mock_request, mock_property_id)
        self.property_repository_mock.find_by_id.assert_called_once_with(
            mock_property_id
        )

        # verify the calls to the repository and service methods
        self.property_repository_mock.find_by_id.assert_called_once_with(
            mock_property_id
        )
        self.update_address_service_mock.execute.assert_called_once_with(
            mock_property.address_id, UpdateAddressRequest(**mock_update_data)
        )

        self.property_repository_mock.update_by_id.assert_called_once_with(
            id=mock_property_id, data=mock_request
        )

    async def test_execute_with_invalid_request_type(self):
        # create a mock request with an invalid type
        mock_request_data = {
            "name": "new name",
            "action": "rent",
            "type": "invalid_type",
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
        mock_request = UpdatePropertyRequest(**mock_request_data)
        mock_property_id = 1

        # mock the repository and service methods
        mock_property = CoroutineMock()
        mock_property.id = 1
        mock_property.address_id = 1
        mock_property.name = "test"
        mock_property.price = 100
        mock_property.type = "apartment"
        mock_property.action = "rent"

        self.property_repository_mock.find_by_id = CoroutineMock()
        self.property_repository_mock.find_by_id.return_value = mock_property

        # call the execute method and assert that the StatusError exception is raised
        with self.assertRaises(StatusError) as context:
            await self.service.execute(mock_request, mock_property_id)

        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(
            context.exception.message, 'field `type` must be "apartment" or "house"'
        )

    async def test_execute_with_invalid_request_action(self):
        # create a mock request with an invalid type
        mock_request_data = {
            "name": "new name",
            "type": "apartment",
            "action": "invalid action",
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
        mock_request = UpdatePropertyRequest(**mock_request_data)
        mock_property_id = 1

        # mock the repository and service methods
        mock_property = CoroutineMock()
        mock_property.id = 1
        mock_property.address_id = 1
        mock_property.name = "test"
        mock_property.price = 100
        mock_property.type = "apartment"
        mock_property.action = "rent"

        self.property_repository_mock.find_by_id = CoroutineMock()
        self.property_repository_mock.find_by_id.return_value = mock_property

        # call the execute method and assert that the StatusError exception is raised
        with self.assertRaises(StatusError) as context:
            await self.service.execute(mock_request, mock_property_id)

        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(
            context.exception.message, 'field `action` must be "rent" or "sale"'
        )

    async def test_raises_not_found(self):
        mock_request_data = {
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
        mock_request = UpdatePropertyRequest(**mock_request_data)
        mock_property_id = 1

        # mock the repository and service methods
        self.property_repository_mock.find_by_id = CoroutineMock()
        self.property_repository_mock.find_by_id.return_value = []

        # call the method and verify the result
        with self.assertRaises(StatusError) as context:
            await self.service.execute(mock_request, mock_property_id)
            self.assertEqual(context.exception.status_code, 422)
            self.assertEqual(
                context.exception.message,
                f"property with `id` {mock_property_id} not found",
            )
