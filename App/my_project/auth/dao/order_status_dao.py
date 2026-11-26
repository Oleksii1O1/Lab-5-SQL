from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.order_status import OrderStatus

class OrderStatusDAO(GeneralDAO):
    _domain_type = OrderStatus

    def find_orders_by_status_id(self, status_id: int):
        status = self.find_by_id(status_id)
        return status.orders if status else None
