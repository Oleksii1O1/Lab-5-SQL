from my_project import db

class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50), nullable=False, index=True)
    street = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(20), nullable=False)
    place_name = db.Column(db.String(100), nullable=True)

    orders = db.relationship('Order', backref='address', lazy=True)

    def put_into_dto(self):
        return {
            'address_id': self.address_id,
            'city': self.city,
            'street': self.street,
            'building': self.building,
            'place_name': self.place_name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Address(
            address_id=dto_dict.get('address_id'),
            city=dto_dict.get('city'),
            street=dto_dict.get('street'),
            building=dto_dict.get('building'),
            place_name=dto_dict.get('place_name')
        )
