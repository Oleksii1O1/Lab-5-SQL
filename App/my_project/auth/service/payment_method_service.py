from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.payment_method_dao import PaymentMethodDAO

class PaymentMethodService(GeneralService):
    def __init__(self):
        self._dao = PaymentMethodDAO()

    def find_payments_by_method_id(self, method_id: int):
        return self._dao.find_payments_by_method_id(method_id)
