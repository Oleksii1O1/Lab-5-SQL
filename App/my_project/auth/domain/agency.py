from my_project import db
from my_project.auth.domain.associations import agency_animators

class Agency(db.Model):
    __tablename__ = 'agencies'

    agency_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=False, index=True)

    orders = db.relationship('Order', backref='agency', lazy=True)
    animators = db.relationship('Animator', secondary=agency_animators, back_populates='agencies')

    def put_into_dto(self):
        return {
            'agency_id': self.agency_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'city': self.city
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Agency(
            agency_id=dto_dict.get('agency_id'),
            name=dto_dict.get('name'),
            phone=dto_dict.get('phone'),
            email=dto_dict.get('email'),
            city=dto_dict.get('city')
        )
