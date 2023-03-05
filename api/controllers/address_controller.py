from fastapi import Depends

from services.address.create_address_service import AddAddressService
from schemas.address_schema import CreateAddressRequest, Address, CreateAddressResponse


class AddressController:
    async def add(
        self,
        request: CreateAddressRequest,
        add_address_service: AddAddressService = Depends(AddAddressService),
    ) -> CreateAddressResponse:
        new_address: Address = await add_address_service.execute(request)
        return CreateAddressResponse(result=new_address)
