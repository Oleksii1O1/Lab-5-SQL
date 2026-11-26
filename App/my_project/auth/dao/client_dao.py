from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.client import Client

class ClientDAO(GeneralDAO):
    _domain_type = Client

    def find_orders_by_client_id(self, client_id: int):
        client = self.find_by_id(client_id)
        return client.orders if client else None
