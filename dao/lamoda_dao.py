from typing import Dict

from config.database import connect_db
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import paginate
from models.lamoda_models import Product

from dao.service_dao import ServiceDao


class LamodaDao(ServiceDao):
    def __init__(self, session: Depends(connect_db)):
        self.session = session
        self.db = session["lamoda"]

    def create(self, product: Product = Body(...)) -> Dict[str, str]:
        encoded_product = jsonable_encoder(product)
        new_product = self.db.insert_one(encoded_product)
        return {"_id": str(new_product.inserted_id), **product.dict()}

    def get_elements_by_category(self, category):
        products = []
        for product in self.db.find({"category": category}):
            products.append(product)
        return paginate(products)
