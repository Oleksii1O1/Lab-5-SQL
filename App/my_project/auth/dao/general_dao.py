from my_project import db

class GeneralDAO:
    _domain_type = None

    def find_all(self):
        return self._domain_type.query.all()

    def find_by_id(self, key):
        return db.session.get(self._domain_type, key)

    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, key, entity_data):
        entity = self.find_by_id(key)
        if not entity:
            return None

        for field, value in entity_data.items():
            if hasattr(entity, field):
                setattr(entity, field, value)

        db.session.commit()
        return entity

    def delete(self, key):
        entity = self.find_by_id(key)
        if not entity:
            return False

        db.session.delete(entity)
        db.session.commit()
        return True
