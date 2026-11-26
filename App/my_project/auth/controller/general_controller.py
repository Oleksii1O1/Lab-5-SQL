class GeneralController:
    _service = None
    _domain_type = None

    def find_all(self):
        entities = self._service.find_all()
        return [entity.put_into_dto() for entity in entities]

    def find_by_id(self, key):
        entity = self._service.find_by_id(key)
        if entity:
            return entity.put_into_dto()
        return None

    def create(self, dto_dict):
        entity = self._domain_type.create_from_dto(dto_dict)
        created = self._service.create(entity)
        return created.put_into_dto()

    def update(self, key, dto_dict):
        updated = self._service.update(key, dto_dict)
        if updated:
            return updated.put_into_dto()
        return None

    def delete(self, key):
        return self._service.delete(key)
