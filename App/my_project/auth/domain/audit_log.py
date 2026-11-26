from datetime import datetime
from my_project import db

def get_kyiv_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo('Europe/Kyiv')).replace(tzinfo=None)
    except Exception:
        from datetime import timezone, timedelta
        return datetime.now(timezone(timedelta(hours=2))).replace(tzinfo=None)

class AnimatorAuditLog(db.Model):
    __tablename__ = 'animator_audit_logs'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animator_id = db.Column(db.Integer, nullable=False, index=True)
    old_hourly_rate = db.Column(db.Numeric(8, 2), nullable=False)
    new_hourly_rate = db.Column(db.Numeric(8, 2), nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False, default=get_kyiv_now)
    details = db.Column(db.String(255), nullable=True)

    def put_into_dto(self):
        return {
            'log_id': self.log_id,
            'animator_id': self.animator_id,
            'old_hourly_rate': float(self.old_hourly_rate) if self.old_hourly_rate is not None else 0.0,
            'new_hourly_rate': float(self.new_hourly_rate) if self.new_hourly_rate is not None else 0.0,
            'modified_at': self.modified_at.strftime('%Y-%m-%d %H:%M:%S') if self.modified_at else None,
            'details': self.details
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return AnimatorAuditLog(
            log_id=dto_dict.get('log_id'),
            animator_id=dto_dict.get('animator_id'),
            old_hourly_rate=dto_dict.get('old_hourly_rate'),
            new_hourly_rate=dto_dict.get('new_hourly_rate'),
            details=dto_dict.get('details')
        )
