from config.database import connect_db
from dao.lamoda_dao import LamodaDao


class LamodaService:
    def __init__(self):
        self.dao = LamodaDao(connect_db())

    def get_all_products(self):
        return self.dao.get_elements()

    def get_all_products_by_category(self, category):
        return self.dao.get_elements_by_category(category)

    def create_product(self, item):
        return self.dao.create(item)

    def get_one_product(self, _id):
        return self.dao.get_element(_id)

    def delete_product(self, _id):
        return self.dao.delete_element(_id)
