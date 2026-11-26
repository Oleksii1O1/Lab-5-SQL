from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.role_dao import RoleDAO

class RoleService(GeneralService):
    def __init__(self):
        self._dao = RoleDAO()
