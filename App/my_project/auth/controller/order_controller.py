from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.order_service import OrderService
from my_project.auth.domain.order import Order

class OrderController(GeneralController):
    def __init__(self):
        self._service = OrderService()
        self._domain_type = Order

    def find_payments_by_order_id(self, order_id: int):
        payments = self._service.find_payments_by_order_id(order_id)
        if payments is None:
            return None
        return [payment.put_into_dto() for payment in payments]

    def find_animators_by_order_id(self, order_id: int):
        return self._service.find_animators_by_order_id(order_id)
