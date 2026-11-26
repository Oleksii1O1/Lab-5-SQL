from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.address_dao import AddressDAO

class AddressService(GeneralService):
    def __init__(self):
        self._dao = AddressDAO()

    def find_orders_by_address_id(self, address_id: int):
        return self._dao.find_orders_by_address_id(address_id)
