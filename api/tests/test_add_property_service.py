# import unittest
# from asynctest import CoroutineMock
# from unittest.mock import patch

# from schemas.property_schemas import CreatePropertyRequest
# from services.property.add_property_service import AddPropertyService

# class TestAddPropertyService(unittest.IsolatedAsyncioTestCase):
#     async def asyncSetUp(self) -> None:
#         self.property_repository = CoroutineMock()
#         self.add_address_service = CoroutineMock()

#         self.service = AddPropertyService(
#             self.property_repository,
#             self.add_address_service,
#         )
     
#     @patch('services.address.create_address_service.AddAddressService.execute')
#     async def test_create_property_with_success(self, mock_execute):
        
#         mock_request =CreatePropertyRequest(
#           **{
#             'name':'test',
#             'action': 'rent',
#             'type': 'house',
#             'description': 'test',
#             'bathrooms': 1,
#             'bedrooms': 2,
#             'price': 1.0,
#             'address': {
#                 'street_name': 'test',
#                 'number': 1,
#                 'cep': '11111-111'
#             },
#             'city': {
#                 'name': 'test',
#                 'state': 'test'
#             }
#           }
#         )
        
#         mock_execute.return_value = {
#             'id': 1,
#             'street_name': 'test',
#             'number': 1,
#             'cep': '11111-111',
#             'city': {
#                 'id': 1,
#                 'name': 'test',
#                 'state': 'test'
#             }
#         }
#         self.property_repository.add = CoroutineMock()

#         await self.service.execute(mock_request)
        
#         mock_execute.assert_called_once()
#         self.property_repository.add.assert_called_once()
