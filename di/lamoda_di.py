from config.database import connect_db
from dao.lamoda_dao import LamodaDao

from di.service_di import Service


class LamodaService(Service):
    def __init__(self):
        self.dao = LamodaDao(connect_db())

    def get_all_products_by_category(self, category):
        return self.dao.get_elements_by_category(category)
