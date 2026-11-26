from my_project import db

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    method_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    payments = db.relationship('Payment', backref='payment_method', lazy=True)

    def put_into_dto(self):
        return {
            'method_id': self.method_id,
            'name': self.name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return PaymentMethod(
            method_id=dto_dict.get('method_id'),
            name=dto_dict.get('name')
        )
