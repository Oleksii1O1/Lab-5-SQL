from my_project import db
from datetime import datetime, date

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.method_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_at = db.Column(db.Date, nullable=False, default=date.today)

    def put_into_dto(self):
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'method_id': self.method_id,
            'amount': float(self.amount) if self.amount is not None else 0.0,
            'paid_at': self.paid_at.strftime('%Y-%m-%d') if self.paid_at else None
        }

    @staticmethod
    def create_from_dto(dto_dict):
        p_date = dto_dict.get('paid_at')
        if isinstance(p_date, str):
            p_date = datetime.strptime(p_date, '%Y-%m-%d').date()
        elif p_date is None:
            p_date = date.today()

        return Payment(
            payment_id=dto_dict.get('payment_id'),
            order_id=dto_dict.get('order_id'),
            method_id=dto_dict.get('method_id'),
            amount=dto_dict.get('amount'),
            paid_at=p_date
        )
