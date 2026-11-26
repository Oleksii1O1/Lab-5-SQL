from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.audit_log import AnimatorAuditLog

class AnimatorAuditLogDAO(GeneralDAO):
    _domain_type = AnimatorAuditLog

    def find_by_animator_id(self, animator_id):
        return AnimatorAuditLog.query.filter_by(animator_id=animator_id).order_by(AnimatorAuditLog.modified_at.desc()).all()
