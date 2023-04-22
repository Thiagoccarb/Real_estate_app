# import warnings

# warnings.filterwarnings("ignore")
# from unittest import IsolatedAsyncioTestCase
# from asynctest import CoroutineMock

# from services.address.update_address_service import UpdateAddressService
# from database.dtos.addresses_dtos import AddressWithCity, UpdateAddress
# from database.dtos.cities_dtos import CreateCity, UpdateCity
# from schemas.address_schema import CreateAddressRequest, Address, UpdateAddressRequest, UpdateAddressResponse
# from schemas.city_schemas import City
# from errors.status_error import StatusError


# class UpdateAddressServiceTests(IsolatedAsyncioTestCase):
#     async def asyncSetUp(self) -> None:
#         self.address_repository = CoroutineMock()
#         self.city_repository = CoroutineMock()
#         self.service = UpdateAddressService(
#             self.address_repository,
#             self.city_repository
#         )

#     async def test_update_address_invalid_cep_format(self):
#     # Arrange
#         request = UpdateAddressRequest(cep="invalid_cep_format")
#         with self.assertRaises(StatusError):
#             await self.service.execute(1, request)
            
#     async def test_update_address_new_city_without_city_data(self):
#         request = UpdateAddressRequest(
#             street_name="New Street",
#             number=456,
#             cep="00000-000",
#             city=UpdateCity()
#         )
#         self.address_repository.find_by_id = CoroutineMock()
#         self.address_repository.update_by_id = CoroutineMock()
#         self.city_repository.find_by = CoroutineMock()
#         self.city_repository.add = CoroutineMock()
#         self.city_repository.find_by_id = CoroutineMock()

#         mock_city = City(name="Test City", state="TS", id=1)
#         self.city_repository.find_by_id.return_value = mock_city
    
#         mock_updated_address = Address(
#           id=1,
#           street_name=request.street_name,
#           city_id=mock_city.id,
#           number=request.number,
#           cep=request.cep,
#         )
        
#         self.address_repository.update_by_id.return_value=mock_updated_address

#         result = await self.service.execute(1, request)
#         self.address_repository.update_by_id.assert_called_once_with(
#           1,
#           UpdateAddress(
#                 street_name=request.street_name,
#                 city_id=mock_city.id,
#                 number=request.number,
#                 cep=request.cep,
#             ),
#         )
#         self.city_repository.find_by.assert_not_called()
#         self.city_repository.add.assert_not_called()
#         self.address_repository.find_by_id.assert_called()
#         self.city_repository.find_by_id.assert_called()
        
#         mock_response = UpdateAddressResponse(
#             street_name=mock_updated_address.street_name,
#             number=mock_updated_address.number,
#             cep=mock_updated_address.cep,
#             city_id=mock_city.id,
#             city=UpdateCity(
#                 name=mock_city.name,
#                 state=mock_city.state,
#             ),
#         )
#         self.assertEqual(result, mock_response)
   
#     async def test_update_address_new_city_with_city_data_and_existing_city_data(self):
#         request = UpdateAddressRequest(
#             street_name="New Street",
#             number=456,
#             cep="00000-000",
#             city=UpdateCity(name='test', state='TS')
#         )
#         self.address_repository.find_by_id = CoroutineMock()
#         self.address_repository.update_by_id = CoroutineMock()
#         self.city_repository.find_by = CoroutineMock()
#         self.city_repository.add = CoroutineMock()
#         self.city_repository.find_by_id = CoroutineMock()

#         mock_city = City(name="Test City", state="TS", id=1)
#         self.city_repository.find_by.return_value = mock_city
    
#         mock_updated_address = Address(
#           id=1,
#           street_name=request.street_name,
#           city_id=mock_city.id,
#           number=request.number,
#           cep=request.cep,
#         )
        
#         self.address_repository.update_by_id.return_value=mock_updated_address

#         result = await self.service.execute(1, request)
#         self.address_repository.update_by_id.assert_called_once_with(
#           1,
#           UpdateAddress(
#                 street_name=request.street_name,
#                 city_id=mock_city.id,
#                 number=request.number,
#                 cep=request.cep,
#             ),
#         )
#         self.city_repository.find_by.assert_called()
#         self.city_repository.add.assert_not_called()
#         self.address_repository.find_by_id.assert_not_called()
#         self.city_repository.find_by_id.assert_not_called()
        
#         mock_response = UpdateAddressResponse(
#             street_name=mock_updated_address.street_name,
#             number=mock_updated_address.number,
#             cep=mock_updated_address.cep,
#             city_id=mock_city.id,
#             city=UpdateCity(
#                 name=request.city.name,
#                 state=request.city.state,
#             ),
#         )
#         self.assertEqual(result, mock_response)
    
#     async def test_update_address_new_city_with_city_data_and_non_existing_city_data(self):
#         request = UpdateAddressRequest(
#             street_name="New Street",
#             number=456,
#             cep="00000-000",
#             city=UpdateCity(name='test', state='TS')
#         )
#         self.address_repository.find_by_id = CoroutineMock()
#         self.address_repository.update_by_id = CoroutineMock()
#         self.city_repository.find_by = CoroutineMock()
#         self.city_repository.add = CoroutineMock()
#         self.city_repository.find_by_id = CoroutineMock()

#         mock_city = City(name="Test City", state="TS", id=1)
#         self.city_repository.find_by.return_value = None
#         self.city_repository.add.return_value = mock_city

#         mock_updated_address = Address(
#           id=1,
#           street_name=request.street_name,
#           city_id=mock_city.id,
#           number=request.number,
#           cep=request.cep,
#         )
        
#         self.address_repository.update_by_id.return_value=mock_updated_address

#         result = await self.service.execute(1, request)
#         self.address_repository.update_by_id.assert_called_once_with(
#           1,
#           UpdateAddress(
#                 street_name=request.street_name,
#                 city_id=mock_city.id,
#                 number=request.number,
#                 cep=request.cep,
#             ),
#         )
#         self.city_repository.find_by.assert_called()
#         self.city_repository.add.assert_called()
#         self.address_repository.find_by_id.assert_not_called()
#         self.city_repository.find_by_id.assert_not_called()
        
#         mock_response = UpdateAddressResponse(
#             street_name=mock_updated_address.street_name,
#             number=mock_updated_address.number,
#             cep=mock_updated_address.cep,
#             city_id=mock_city.id,
#             city=UpdateCity(
#                 name=request.city.name,
#                 state=request.city.state,
#             ),
#         )
#         self.assertEqual(result, mock_response)
