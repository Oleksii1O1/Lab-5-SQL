from my_project import db

class HolidayType(db.Model):
    __tablename__ = 'holiday_types'

    holiday_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    orders = db.relationship('Order', backref='holiday_type', lazy=True)

    def put_into_dto(self):
        return {
            'holiday_type_id': self.holiday_type_id,
            'name': self.name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return HolidayType(
            holiday_type_id=dto_dict.get('holiday_type_id'),
            name=dto_dict.get('name')
        )
