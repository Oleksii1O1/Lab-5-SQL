from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.payment_service import PaymentService
from my_project.auth.domain.payment import Payment

class PaymentController(GeneralController):
    def __init__(self):
        self._service = PaymentService()
        self._domain_type = Payment
