from fastapi import Depends, Header

from services.auth.auth import AuthService
from services.address.create_address_service import AddAddressService
from schemas.address_schema import CreateAddressRequest, Address, CreateAddressResponse


class AddressController:
    async def add(
        self,
        request: CreateAddressRequest,
        add_address_service: AddAddressService = Depends(AddAddressService),
        auth_service: AuthService = Depends(AuthService),
        authorization = Header(None)
    ) -> CreateAddressResponse:
        await auth_service.execute( authorization=authorization, decode=True)
        new_address: Address = await add_address_service.execute(request)
        return CreateAddressResponse(result=new_address)
