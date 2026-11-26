from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.payment_method_service import PaymentMethodService
from my_project.auth.domain.payment_method import PaymentMethod

class PaymentMethodController(GeneralController):
    def __init__(self):
        self._service = PaymentMethodService()
        self._domain_type = PaymentMethod

    def find_payments_by_method_id(self, method_id: int):
        payments = self._service.find_payments_by_method_id(method_id)
        if payments is None:
            return None
        return [payment.put_into_dto() for payment in payments]
