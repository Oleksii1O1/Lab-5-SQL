from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.agency_service import AgencyService
from my_project.auth.domain.agency import Agency

class AgencyController(GeneralController):
    def __init__(self):
        self._service = AgencyService()
        self._domain_type = Agency

    def find_orders_by_agency_id(self, agency_id: int):
        orders = self._service.find_orders_by_agency_id(agency_id)
        if orders is None:
            return None
        return [order.put_into_dto() for order in orders]

    def find_animators_by_agency_id(self, agency_id: int):
        animators = self._service.find_animators_by_agency_id(agency_id)
        if animators is None:
            return None
        return [animator.put_into_dto() for animator in animators]
