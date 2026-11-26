from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.order_status_service import OrderStatusService
from my_project.auth.domain.order_status import OrderStatus

class OrderStatusController(GeneralController):
    def __init__(self):
        self._service = OrderStatusService()
        self._domain_type = OrderStatus

    def find_orders_by_status_id(self, status_id: int):
        orders = self._service.find_orders_by_status_id(status_id)
        if orders is None:
            return None
        return [order.put_into_dto() for order in orders]
