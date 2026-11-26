from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.specialization_dao import SpecializationDAO

class SpecializationService(GeneralService):
    def __init__(self):
        self._dao = SpecializationDAO()

    def find_animators_by_specialization_id(self, specialization_id: int):
        return self._dao.find_animators_by_specialization_id(specialization_id)
