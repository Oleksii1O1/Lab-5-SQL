from my_project import db
from my_project.auth.domain.associations import animator_specializations

class Specialization(db.Model):
    __tablename__ = 'specializations'

    specialization_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    animators = db.relationship('Animator', secondary=animator_specializations, back_populates='specializations')

    def put_into_dto(self):
        return {
            'specialization_id': self.specialization_id,
            'name': self.name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Specialization(
            specialization_id=dto_dict.get('specialization_id'),
            name=dto_dict.get('name')
        )
