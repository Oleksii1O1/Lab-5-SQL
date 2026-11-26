from my_project import db

class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)

    orders = db.relationship('Order', backref='client', lazy=True)

    def put_into_dto(self):
        return {
            'client_id': self.client_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return Client(
            client_id=dto_dict.get('client_id'),
            full_name=dto_dict.get('full_name'),
            phone=dto_dict.get('phone'),
            email=dto_dict.get('email')
        )
