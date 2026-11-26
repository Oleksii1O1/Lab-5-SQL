from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.specialization import Specialization

class SpecializationDAO(GeneralDAO):
    _domain_type = Specialization

    def find_animators_by_specialization_id(self, specialization_id: int):
        specialization = self.find_by_id(specialization_id)
        return specialization.animators if specialization else None
