from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.payment import Payment

class PaymentDAO(GeneralDAO):
    _domain_type = Payment
