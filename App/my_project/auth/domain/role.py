from my_project import db

class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def put_into_dto(self):
        return {
            'role_id': self.role_id,
            'name': self.name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Role(
            role_id=dto_dict.get('role_id'),
            name=dto_dict.get('name')
        )
