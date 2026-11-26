from my_project import db
from datetime import date, datetime

class Review(db.Model):
    __tablename__ = 'animator_reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animator_id = db.Column(db.Integer, nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    review_date = db.Column(db.Date, nullable=False, default=date.today)

    def put_into_dto(self):
        return {
            'review_id': self.review_id,
            'animator_id': self.animator_id,
            'rating': self.rating,
            'comment': self.comment,
            'review_date': self.review_date.isoformat() if self.review_date else None
        }

    @staticmethod
    def create_from_dto(dto_dict):
        r_date = dto_dict.get('review_date')
        if isinstance(r_date, str):
            r_date = datetime.strptime(r_date, '%Y-%m-%d').date()
        elif r_date is None:
            r_date = date.today()

        return Review(
            review_id=dto_dict.get('review_id'),
            animator_id=dto_dict.get('animator_id'),
            rating=dto_dict.get('rating'),
            comment=dto_dict.get('comment'),
            review_date=r_date
        )
