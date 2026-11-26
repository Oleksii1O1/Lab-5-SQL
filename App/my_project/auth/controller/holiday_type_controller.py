from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.holiday_type_service import HolidayTypeService
from my_project.auth.domain.holiday_type import HolidayType

class HolidayTypeController(GeneralController):
    def __init__(self):
        self._service = HolidayTypeService()
        self._domain_type = HolidayType

    def find_orders_by_holiday_type_id(self, holiday_type_id: int):
        orders = self._service.find_orders_by_holiday_type_id(holiday_type_id)
        if orders is None:
            return None
        return [order.put_into_dto() for order in orders]
