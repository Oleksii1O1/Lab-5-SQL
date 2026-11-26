from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.holiday_type_dao import HolidayTypeDAO

class HolidayTypeService(GeneralService):
    def __init__(self):
        self._dao = HolidayTypeDAO()

    def find_orders_by_holiday_type_id(self, holiday_type_id: int):
        return self._dao.find_orders_by_holiday_type_id(holiday_type_id)
