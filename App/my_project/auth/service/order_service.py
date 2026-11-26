from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.order_dao import OrderDAO

class OrderService(GeneralService):
    def __init__(self):
        self._dao = OrderDAO()

    def find_payments_by_order_id(self, order_id: int):
        return self._dao.find_payments_by_order_id(order_id)

    def find_animators_by_order_id(self, order_id: int):
        return self._dao.find_animators_by_order_id(order_id)
