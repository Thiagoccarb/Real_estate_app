import unittest
from unittest.mock import MagicMock

from schemas.image_schemas import Image
from database.repositories.address_repository import AddressesRepository
from database.repositories.image_repository import ImagesRepository
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError
from schemas.property_schemas import Property
from utils.backblaze_b2 import B2skd

from services.property.remove_property_service import RemovePropertyService


class TestRemovePropertyService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.property_repository_mock = MagicMock(spec=PropertiesRepository)
        self.address_repository_mock = MagicMock(spec=AddressesRepository)
        self.image_repository_mock = MagicMock(spec=ImagesRepository)
        self.b2_mock = MagicMock(spec=B2skd)

        self.service = RemovePropertyService(
            property_repository=self.property_repository_mock,
            address_repository=self.address_repository_mock,
            image_repository=self.image_repository_mock,
            b2=self.b2_mock,
        )

    async def test_execute_with_valid_id(self):
        # Mock the property and image repositories to return valid data
        self.property_repository_mock.find_by_id.return_value = Property(
            id=1,
            name="Test Property",
            bedrooms=2,
            bathrooms=1,
            description="Test Description",
        )
        self.image_repository_mock.find_all_by_property_id.return_value = [
            Image(id=1, audio_hash="test_hash_1", url="test-url-1"),
            Image(id=2, audio_hash="test_hash_2", url="test-url-2"),
        ]

        # Call the remove property service with a valid ID
        await self.service.execute(id=1)

        # Verify that the remove operations were called with the expected IDs
        self.property_repository_mock.remove_by_id.assert_called_once_with(1)
        self.image_repository_mock.remove_by_property_id.assert_not_called()

    async def test_execute_with_invalid_id(self):
        # Mock the property repository to return None for a non-existent ID
        self.property_repository_mock.find_by_id.return_value = None

        # Call the remove property service with an invalid ID
        with self.assertRaises(StatusError):
            await self.service.execute(id=1)

        # Verify that the remove operations were not called
        self.property_repository_mock.remove_by_id.assert_not_called()
        self.image_repository_mock.remove_by_property_id.assert_not_called()
        self.b2_mock.delete_file_by_audio_hash.assert_not_called()
