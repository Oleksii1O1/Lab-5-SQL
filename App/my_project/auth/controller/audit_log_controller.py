from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.audit_log_service import AnimatorAuditLogService
from my_project.auth.domain.audit_log import AnimatorAuditLog

class AnimatorAuditLogController(GeneralController):
    def __init__(self):
        self._service = AnimatorAuditLogService()
        self._domain_type = AnimatorAuditLog

    def find_by_animator_id(self, animator_id: int):
        logs = self._service.get_by_animator_id(animator_id)
        return [l.put_into_dto() for l in logs]
