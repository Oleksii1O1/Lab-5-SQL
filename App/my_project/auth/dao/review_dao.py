from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.review import Review

class ReviewDAO(GeneralDAO):
    _domain_type = Review

    def find_by_animator_id(self, animator_id):
        return Review.query.filter_by(animator_id=animator_id).all()
