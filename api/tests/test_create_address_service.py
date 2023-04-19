import warnings
warnings.filterwarnings("ignore")
from unittest import IsolatedAsyncioTestCase
from asynctest import CoroutineMock

from database.dtos.addresses_dtos import AddressWithCity
from database.dtos.cities_dtos import CreateCity
from schemas.address_schema import CreateAddressRequest, Address
from schemas.city_schemas import City
from api.services.address.create_address_service import AddAddressService
from errors.status_error import StatusError


class AddAddressServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.address_repository = CoroutineMock()
        self.city_repository = CoroutineMock()
        self.service = AddAddressService(
            self.address_repository,
            self.city_repository
        )

    async def test_add_address(self):
        mock_request = CreateAddressRequest(
            street_name='test',
            cep='11111-111', 
            city_data=CreateCity(name='test', state='AB')
        )

        # Test if city is not found
        self.city_repository.find_by = CoroutineMock()
        self.city_repository.find_by.return_value = None

        self.city_repository.add = CoroutineMock()
        self.city_repository.add.return_value = City(
            id=1,
            name='test',
            state='AB'
        )

        self.address_repository.add = CoroutineMock()
        self.address_repository.add.return_value = Address(
            id=1,
            street_name='test',
            city_id=1,
            cep='11111-111'
        )

        response = await self.service.execute(mock_request)
        self.assertEqual(response, AddressWithCity(**{
            **Address(
                id=1,
                street_name='test',
                city_id=1,
                cep='11111-111'
            ).dict(),
            "city": {**City(
                id=1,
                name='test',
                state='AB'
            ).dict(exclude={"id"})}
        }))

        # Test if city is found
        self.city_repository.find_by.return_value = City(
            id=1,
            name='test',
            state='AB'
        )

        response = await self.service.execute(mock_request)
        self.assertEqual(response, AddressWithCity(**{
            **Address(
                id=1,
                street_name='test',
                city_id=1,
                cep='11111-111'
            ).dict(),
            "city": {**City(
                id=1,
                name='test',
                state='AB'
            ).dict(exclude={"id"})}
        }))

        # Test with invalid cep
        mock_request = CreateAddressRequest(
            street_name='test',
            cep='11111',  # Invalid cep format
            city_data=CreateCity(name='test', state='AB')
        )

        with self.assertRaises(StatusError):
            await self.service.execute(mock_request)

        mock_request = CreateAddressRequest(
            street_name='test',
            cep='11111-',  # Invalid cep format
            city_data=CreateCity(name='test', state='AB')
        )

        with self.assertRaises(StatusError):
            await self.service.execute(mock_request)

        mock_request = CreateAddressRequest(
            street_name='test',
            cep='11111-1111',  # Invalid cep format
            city_data=CreateCity(name='test', state='AB')
        )

        with self.assertRaises(StatusError):
            await self.service.execute(mock_request)
