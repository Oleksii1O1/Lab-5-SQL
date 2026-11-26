from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.payment_method import PaymentMethod

class PaymentMethodDAO(GeneralDAO):
    _domain_type = PaymentMethod

    def find_payments_by_method_id(self, method_id: int):
        method = self.find_by_id(method_id)
        return method.payments if method else None
