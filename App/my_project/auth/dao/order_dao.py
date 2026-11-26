from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.order import Order

class OrderDAO(GeneralDAO):
    _domain_type = Order

    def find_payments_by_order_id(self, order_id: int):
        order = self.find_by_id(order_id)
        return order.payments if order else None

    def find_animators_by_order_id(self, order_id: int):
        order = self.find_by_id(order_id)
        if not order:
            return None
        return [assignment.put_into_dto() for assignment in order.animator_assignments]
