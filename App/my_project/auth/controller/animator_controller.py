from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.animator_service import AnimatorService
from my_project.auth.domain.animator import Animator

class AnimatorController(GeneralController):
    def __init__(self):
        self._service = AnimatorService()
        self._domain_type = Animator

    def find_agencies_by_animator_id(self, animator_id: int):
        agencies = self._service.find_agencies_by_animator_id(animator_id)
        if agencies is None:
            return None
        return [agency.put_into_dto() for agency in agencies]

    def find_specializations_by_animator_id(self, animator_id: int):
        specs = self._service.find_specializations_by_animator_id(animator_id)
        if specs is None:
            return None
        return [s.put_into_dto() for s in specs]
