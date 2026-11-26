from my_project import db
from datetime import datetime, date, time

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.agency_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    holiday_type_id = db.Column(db.Integer, db.ForeignKey('holiday_types.holiday_type_id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.status_id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)

    payments = db.relationship('Payment', backref='order', lazy=True, cascade='all, delete-orphan')
    animator_assignments = db.relationship('OrderAnimator', lazy='joined', cascade='all, delete-orphan')

    def put_into_dto(self):
        return {
            'order_id': self.order_id,
            'agency_id': self.agency_id,
            'client_id': self.client_id,
            'holiday_type_id': self.holiday_type_id,
            'address_id': self.address_id,
            'status_id': self.status_id,
            'event_date': self.event_date.strftime('%Y-%m-%d') if self.event_date else None,
            'start_time': str(self.start_time) if self.start_time else None,
            'duration_minutes': self.duration_minutes,
            'total_cost': float(self.total_cost) if self.total_cost is not None else 0.0
        }

    @staticmethod
    def create_from_dto(dto_dict):
        e_date = dto_dict.get('event_date')
        if isinstance(e_date, str):
            e_date = datetime.strptime(e_date, '%Y-%m-%d').date()

        s_time = dto_dict.get('start_time')
        if isinstance(s_time, str):
            parts = [int(p) for p in s_time.split(':')]
            if len(parts) == 2:
                s_time = time(parts[0], parts[1])
            elif len(parts) == 3:
                s_time = time(parts[0], parts[1], parts[2])

        return Order(
            order_id=dto_dict.get('order_id'),
            agency_id=dto_dict.get('agency_id'),
            client_id=dto_dict.get('client_id'),
            holiday_type_id=dto_dict.get('holiday_type_id'),
            address_id=dto_dict.get('address_id'),
            status_id=dto_dict.get('status_id'),
            event_date=e_date,
            start_time=s_time,
            duration_minutes=dto_dict.get('duration_minutes'),
            total_cost=dto_dict.get('total_cost')
        )
