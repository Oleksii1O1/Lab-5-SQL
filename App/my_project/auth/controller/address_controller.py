from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.address_service import AddressService
from my_project.auth.domain.address import Address

class AddressController(GeneralController):
    def __init__(self):
        self._service = AddressService()
        self._domain_type = Address

    def find_orders_by_address_id(self, address_id: int):
        orders = self._service.find_orders_by_address_id(address_id)
        if orders is None:
            return None
        return [order.put_into_dto() for order in orders]
