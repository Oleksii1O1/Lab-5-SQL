from my_project import db
from datetime import date

agency_animators = db.Table(
    'agency_animators',
    db.Column('agency_id', db.Integer, db.ForeignKey('agencies.agency_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('animator_id', db.Integer, db.ForeignKey('animators.animator_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('cooperation_start', db.Date, nullable=False, default=date.today)
)

animator_specializations = db.Table(
    'animator_specializations',
    db.Column('animator_id', db.Integer, db.ForeignKey('animators.animator_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('specialization_id', db.Integer, db.ForeignKey('specializations.specialization_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)

class OrderAnimator(db.Model):
    __tablename__ = 'order_animators'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    animator_id = db.Column(db.Integer, db.ForeignKey('animators.animator_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    fee = db.Column(db.Numeric(10, 2), nullable=False)

    role = db.relationship('Role', lazy='joined')
    animator = db.relationship('Animator', lazy='joined')

    def put_into_dto(self):
        return {
            'order_id': self.order_id,
            'animator_id': self.animator_id,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'animator_name': f"{self.animator.first_name} {self.animator.last_name}" if self.animator else None,
            'fee': float(self.fee) if self.fee is not None else 0.0
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return OrderAnimator(
            order_id=dto_dict.get('order_id'),
            animator_id=dto_dict.get('animator_id'),
            role_id=dto_dict.get('role_id'),
            fee=dto_dict.get('fee')
        )
