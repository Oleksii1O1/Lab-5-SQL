from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.payment_dao import PaymentDAO

class PaymentService(GeneralService):
    def __init__(self):
        self._dao = PaymentDAO()
