from datetime import datetime
from my_project import db
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.animator import Animator
from my_project.auth.domain.audit_log import AnimatorAuditLog, get_kyiv_now

class AnimatorDAO(GeneralDAO):
    _domain_type = Animator

    def find_agencies_by_animator_id(self, animator_id: int):
        animator = self.find_by_id(animator_id)
        return animator.agencies if animator else None

    def find_specializations_by_animator_id(self, animator_id: int):
        animator = self.find_by_id(animator_id)
        return animator.specializations if animator else None

    def update(self, key, entity_data):
        animator = self.find_by_id(key)
        if not animator:
            return None

        old_rate = float(animator.hourly_rate) if animator.hourly_rate is not None else 0.0

        updated = super().update(key, entity_data)

        if updated and 'hourly_rate' in entity_data:
            try:
                new_rate = float(updated.hourly_rate) if updated.hourly_rate is not None else 0.0
                if old_rate != new_rate:

                    existing = AnimatorAuditLog.query.filter_by(
                        animator_id=updated.animator_id,
                        old_hourly_rate=old_rate,
                        new_hourly_rate=new_rate
                    ).first()

                    if not existing:
                        log = AnimatorAuditLog(
                            animator_id=updated.animator_id,
                            old_hourly_rate=old_rate,
                            new_hourly_rate=new_rate,
                            modified_at=get_kyiv_now(),
                            details=f"Hourly rate changed from {old_rate} to {new_rate}"
                        )
                        db.session.add(log)
                        db.session.commit()
            except Exception:
                pass

        return updated
