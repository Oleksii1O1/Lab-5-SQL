from my_project.auth.dao.procedure_dao import ProcedureDAO

class ProcedureService:
    _dao = ProcedureDAO()

    def execute_insert_client(self, full_name, phone, email):
        if not full_name or not phone:
            raise ValueError("Full name and phone are required")
        return self._dao.insert_client_proc(full_name, phone, email)

    def execute_link_m2m(self, first_name, last_name, specialization_name):
        if not first_name or not last_name or not specialization_name:
            raise ValueError("first_name, last_name, and specialization_name are required")
        return self._dao.link_m2m_proc(first_name, last_name, specialization_name)

    def execute_insert_ten_nonames(self):
        return self._dao.insert_ten_nonames_proc()

    def execute_get_animators_above_avg(self):
        return self._dao.get_animators_above_avg_proc()

    def execute_cursor_split(self):
        return self._dao.cursor_split_animators_proc()
