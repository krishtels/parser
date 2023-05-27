from abc import ABC


class Service(ABC):
    def __init__(self, dao):
        self.dao = dao

    def get_all_products(self):
        return self.dao.get_elements()

    def create_product(self, item):
        return self.dao.create(item)

    def get_one_product(self, _id):
        return self.dao.get_element(_id)

    def delete_product(self, _id):
        return self.dao.delete_element(_id)
