from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.address import Address

class AddressDAO(GeneralDAO):
    _domain_type = Address

    def find_orders_by_address_id(self, address_id: int):
        address = self.find_by_id(address_id)
        return address.orders if address else None
