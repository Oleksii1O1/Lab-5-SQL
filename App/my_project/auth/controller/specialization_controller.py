from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.specialization_service import SpecializationService
from my_project.auth.domain.specialization import Specialization

class SpecializationController(GeneralController):
    def __init__(self):
        self._service = SpecializationService()
        self._domain_type = Specialization

    def find_animators_by_specialization_id(self, specialization_id: int):
        animators = self._service.find_animators_by_specialization_id(specialization_id)
        if animators is None:
            return None
        return [animator.put_into_dto() for animator in animators]
