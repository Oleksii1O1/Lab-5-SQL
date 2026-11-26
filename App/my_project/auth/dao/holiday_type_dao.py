from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.holiday_type import HolidayType

class HolidayTypeDAO(GeneralDAO):
    _domain_type = HolidayType

    def find_orders_by_holiday_type_id(self, holiday_type_id: int):
        holiday_type = self.find_by_id(holiday_type_id)
        return holiday_type.orders if holiday_type else None
