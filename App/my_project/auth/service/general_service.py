class GeneralService:
    _dao = None

    def find_all(self):
        return self._dao.find_all()

    def find_by_id(self, key):
        return self._dao.find_by_id(key)

    def create(self, entity):
        return self._dao.create(entity)

    def update(self, key, entity_data):
        return self._dao.update(key, entity_data)

    def delete(self, key):
        return self._dao.delete(key)
