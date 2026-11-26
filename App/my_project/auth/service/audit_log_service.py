from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.audit_log_dao import AnimatorAuditLogDAO

class AnimatorAuditLogService(GeneralService):
    _dao = AnimatorAuditLogDAO()

    def get_by_animator_id(self, animator_id):
        return self._dao.find_by_animator_id(animator_id)
