import pytest
from unittest.mock import MagicMock

from errors.status_error import StatusError
from schemas.property_schemas import CreatePropertyRequest, Property
from services.property.add_property_service import AddPropertyService


@pytest.fixture
def fake_properties_repo():
    class FakePropertiesRepo:
        async def add(self, data: CreatePropertyRequest) -> Property:
            return Property(
                id=1,
                name=data.name,
                action=data.action,
                type=data.type,
                address_id=data.address_id,
            )

    return FakePropertiesRepo()


@pytest.fixture
def fake_addresses_repo():
    class FakeAddressesRepo:
        async def find_by_id(self, id: int):
            if id == 1:
                return MagicMock()
            else:
                return None

    return FakeAddressesRepo()


@pytest.fixture
def add_property_service(fake_properties_repo, fake_addresses_repo):
    return AddPropertyService(
        property_repository=fake_properties_repo,
        address_repository=fake_addresses_repo,
    )


@pytest.mark.asyncio
async def test_add_property_service_valid_request(add_property_service):
    request = CreatePropertyRequest(
        name="Test Property",
        action="rent",
        type="apartment",
        address_id=1,
    )

    response = await add_property_service.execute(request)

    assert response.id == 1
    assert response.name == request.name
    assert response.action == request.action
    assert response.type == request.type
    assert response.address_id == request.address_id


@pytest.mark.asyncio
async def test_add_property_service_invalid_type(add_property_service):
    request = CreatePropertyRequest(
        name="Test Property",
        action="rent",
        type="invalid",
        address_id=1,
    )

    with pytest.raises(StatusError):
        await add_property_service.execute(request)


@pytest.mark.asyncio
async def test_add_property_service_invalid_action(add_property_service):
    request = CreatePropertyRequest(
        name="Test Property",
        action="invalid",
        type="apartment",
        address_id=1,
    )

    with pytest.raises(StatusError):
        await add_property_service.execute(request)


@pytest.mark.asyncio
async def test_add_property_service_invalid_address_id(add_property_service):
    request = CreatePropertyRequest(
        name="Test Property",
        action="rent",
        type="apartment",
        address_id=2,
    )

    with pytest.raises(StatusError):
        await add_property_service.execute(request)
