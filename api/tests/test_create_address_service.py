import pytest

from errors.status_error import StatusError
from schemas.address_schema import Address, CreateAddressRequest
from services.address.create_address_service import AddAddressService


@pytest.fixture
def fake_addresses_repo():
    class FakeAddressesRepo:
        async def add(self, request: CreateAddressRequest) -> Address:
            return Address(
                id=1,
                street_name=request.street_name,
                city_id=request.city_id,
                number=request.number,
                cep=request.cep,
            )

    return FakeAddressesRepo()


@pytest.fixture
def fake_cities_repo():
    class FakeCitiesRepo:
        async def find_by_id(self, id: int):
            if id == 1:
                return {"id": 1, "name": "Test City"}
            else:
                return None

    return FakeCitiesRepo()


@pytest.fixture
def add_address_service(fake_addresses_repo, fake_cities_repo):
    return AddAddressService(
        address_repository=fake_addresses_repo,
        city_repository=fake_cities_repo,
    )


@pytest.mark.asyncio
async def test_add_address_service(add_address_service):
    request = CreateAddressRequest(
        street_name="Test Street",
        city_id=1,
        number=123,
        cep="12345-678",
    )
    response = await add_address_service.execute(request)
    assert response.id == 1
    assert response.street_name == request.street_name
    assert response.city_id == request.city_id
    assert response.number == str(request.number)
    assert response.cep == request.cep

    with pytest.raises(StatusError):
        request = CreateAddressRequest(
            street_name="Test Street",
            city_id=2,
            number=123,
            cep="12345-678",
        )
        await add_address_service.execute(request)

    with pytest.raises(StatusError):
        request = CreateAddressRequest(
            street_name="Test Street",
            city_id=1,
            number="123",
            cep="invalid_cep",
        )
        await add_address_service.execute(request)
