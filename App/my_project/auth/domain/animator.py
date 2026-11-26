from my_project import db
from my_project.auth.domain.associations import agency_animators, animator_specializations

class Animator(db.Model):
    __tablename__ = 'animators'

    animator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    hourly_rate = db.Column(db.Numeric(8, 2), nullable=False)

    agencies = db.relationship('Agency', secondary=agency_animators, back_populates='animators')
    specializations = db.relationship('Specialization', secondary=animator_specializations, back_populates='animators')

    def put_into_dto(self):
        return {
            'animator_id': self.animator_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate is not None else 0.0
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Animator(
            animator_id=dto_dict.get('animator_id'),
            first_name=dto_dict.get('first_name'),
            last_name=dto_dict.get('last_name'),
            phone=dto_dict.get('phone'),
            email=dto_dict.get('email'),
            hourly_rate=dto_dict.get('hourly_rate')
        )
