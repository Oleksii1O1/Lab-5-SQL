from my_project.auth.service.procedure_service import ProcedureService

class ProcedureController:
    def __init__(self):
        self._service = ProcedureService()

    def insert_client(self, data):
        full_name = data.get('full_name')
        phone = data.get('phone')
        email = data.get('email')
        return self._service.execute_insert_client(full_name, phone, email)

    def link_m2m(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        specialization_name = data.get('specialization_name')
        return self._service.execute_link_m2m(first_name, last_name, specialization_name)

    def insert_ten_nonames(self):
        return self._service.execute_insert_ten_nonames()

    def get_animators_above_avg(self):
        return self._service.execute_get_animators_above_avg()

    def cursor_split(self):
        return self._service.execute_cursor_split()
