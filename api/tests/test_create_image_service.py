import pytest
import base64

from errors.status_error import StatusError
from services.image.create_image_service import AddImageService
from schemas.image_schemas import CreateImageRequest


@pytest.fixture
def fake_images_repository():
    class FakeImagesRepository:
        async def add(self, data):
            return 1

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
def add_image_service(fake_images_repository, fake_properties_repository):
    return AddImageService(
        image_repository=fake_images_repository,
        property_repository=fake_properties_repository,
    )


@pytest.mark.asyncio
async def test_add_image_service(add_image_service):
    # Test valid request
    request = CreateImageRequest(
        property_id=1,
        str_binary=base64.b64encode(b"Test Binary").decode(),
    )
    response = await add_image_service.execute(request)
    assert response == 1

    # Test invalid property ID
    request = CreateImageRequest(
        property_id=2,
        str_binary=base64.b64encode(b"Test Binary").decode(),
    )
    with pytest.raises(StatusError):
        await add_image_service.execute(request)

    # Test invalid binary string
    request = CreateImageRequest(
        property_id=1,
        str_binary="Invalid Binary",
    )
    with pytest.raises(StatusError):
        await add_image_service.execute(request)
