from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.role import Role

class RoleDAO(GeneralDAO):
    _domain_type = Role
