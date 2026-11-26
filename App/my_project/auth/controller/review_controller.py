from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.review_service import ReviewService
from my_project.auth.domain.review import Review

class ReviewController(GeneralController):
    def __init__(self):
        self._service = ReviewService()
        self._domain_type = Review

    def find_by_animator_id(self, animator_id: int):
        reviews = self._service.get_by_animator_id(animator_id)
        return [r.put_into_dto() for r in reviews]
