from my_project import db

class OrderStatus(db.Model):
    __tablename__ = 'order_statuses'

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    orders = db.relationship('Order', backref='status', lazy=True)

    def put_into_dto(self):
        return {
            'status_id': self.status_id,
            'name': self.name
        }

    @staticmethod
    def create_from_dto(dto_dict):
        return OrderStatus(
            status_id=dto_dict.get('status_id'),
            name=dto_dict.get('name')
        )
