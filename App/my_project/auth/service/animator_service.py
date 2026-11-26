from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.animator_dao import AnimatorDAO

class AnimatorService(GeneralService):
    def __init__(self):
        self._dao = AnimatorDAO()

    def find_agencies_by_animator_id(self, animator_id: int):
        return self._dao.find_agencies_by_animator_id(animator_id)

    def find_specializations_by_animator_id(self, animator_id: int):
        return self._dao.find_specializations_by_animator_id(animator_id)
