from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.order_status_dao import OrderStatusDAO

class OrderStatusService(GeneralService):
    def __init__(self):
        self._dao = OrderStatusDAO()

    def find_orders_by_status_id(self, status_id: int):
        return self._dao.find_orders_by_status_id(status_id)
