from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.agency_dao import AgencyDAO

class AgencyService(GeneralService):
    def __init__(self):
        self._dao = AgencyDAO()

    def find_orders_by_agency_id(self, agency_id: int):
        return self._dao.find_orders_by_agency_id(agency_id)

    def find_animators_by_agency_id(self, agency_id: int):
        return self._dao.find_animators_by_agency_id(agency_id)
