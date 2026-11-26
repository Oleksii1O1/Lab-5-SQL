from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.review_dao import ReviewDAO

class ReviewService(GeneralService):
    _dao = ReviewDAO()

    def get_by_animator_id(self, animator_id):
        return self._dao.find_by_animator_id(animator_id)
