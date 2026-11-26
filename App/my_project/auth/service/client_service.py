from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.client_dao import ClientDAO

class ClientService(GeneralService):
    def __init__(self):
        self._dao = ClientDAO()

    def find_orders_by_client_id(self, client_id: int):
        return self._dao.find_orders_by_client_id(client_id)
