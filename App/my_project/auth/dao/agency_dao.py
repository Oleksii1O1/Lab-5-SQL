from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.agency import Agency

class AgencyDAO(GeneralDAO):
    _domain_type = Agency

    def find_orders_by_agency_id(self, agency_id: int):
        agency = self.find_by_id(agency_id)
        return agency.orders if agency else None

    def find_animators_by_agency_id(self, agency_id: int):
        agency = self.find_by_id(agency_id)
        return agency.animators if agency else None
