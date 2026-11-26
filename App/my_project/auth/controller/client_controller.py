from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.client_service import ClientService
from my_project.auth.domain.client import Client

class ClientController(GeneralController):
    def __init__(self):
        self._service = ClientService()
        self._domain_type = Client

    def find_orders_by_client_id(self, client_id: int):
        orders = self._service.find_orders_by_client_id(client_id)
        if orders is None:
            return None
        return [order.put_into_dto() for order in orders]
