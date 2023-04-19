import pytest
import base64
from unittest.mock import AsyncMock, MagicMock

from api.services.image.batch_create_image_service import BatchAddImageService
from errors.status_error import StatusError
from schemas.image_schemas import BatchCreateImageRequest


@pytest.fixture
def fake_images_repository():
    class FakeImagesRepository:
        async def find_by_audio_hash(self, audio_hash):
            return None

        async def add(self, data):
            return {"id": 1}

        async def update_position(self, image_id, position):
            pass

    return FakeImagesRepository()


@pytest.fixture
def fake_properties_repository():
    class FakePropertiesRepository:
        async def find_by_id(self, id):
            if id == 1:
                return {"id": 1, "name": "Test Property"}
            else:
                return None

    return FakePropertiesRepository()


@pytest.fixture
def mock_b2skd():
    mock_instance = MagicMock()
    mock_instance.upload_binary_to_blackblaze.return_value = AsyncMock()
    mock_instance.get_download_url.return_value = "http://test-url.com"
    return mock_instance


@pytest.fixture
def batch_add_image_service(fake_images_repository, fake_properties_repository, mock_b2skd):
    return BatchAddImageService(
        image_repository=fake_images_repository,
        property_repository=fake_properties_repository,
        b2=mock_b2skd,
    )


@pytest.mark.asyncio
async def test_batch_add_image_service(batch_add_image_service):
    # Test valid request with one image
    request = BatchCreateImageRequest(
        property_id=1,
        list_str_binary=[base64.b64encode(b"Test Binary").decode()],
    )
    response = await batch_add_image_service.execute(request)
    assert len(response) == 1
    assert response[0]["id"] == 1

    # Test valid request with multiple images
    request = BatchCreateImageRequest(
        property_id=1,
        list_str_binary=[
            base64.b64encode(b"Test Binary 1").decode(),
            base64.b64encode(b"Test Binary 2").decode(),
            base64.b64encode(b"Test Binary 3").decode(),
        ],
    )
    response = await batch_add_image_service.execute(request)
    assert len(response) == 3
    assert response[0]["id"] == 1
    assert response[1]["id"] == 1
    assert response[2]["id"] == 1

    # Test invalid property ID
    request = BatchCreateImageRequest(
        property_id=2,
        list_str_binary=[base64.b64encode(b"Test Binary").decode()],
    )
    with pytest.raises(StatusError):
        await batch_add_image_service.execute(request)

    # Test invalid binary string
    request = BatchCreateImageRequest(
        property_id=1,
        list_str_binary=["Invalid Binary"],
    )
    with pytest.raises(StatusError):
        await batch_add_image_service.execute(request)
