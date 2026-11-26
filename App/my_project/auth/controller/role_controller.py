from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.role_service import RoleService
from my_project.auth.domain.role import Role

class RoleController(GeneralController):
    def __init__(self):
        self._service = RoleService()
        self._domain_type = Role
