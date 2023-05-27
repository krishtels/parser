from typing import Dict

from bson import ObjectId
from config.database import connect_db
from fastapi import Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import paginate
from kafka import KafkaConsumer
from models.lamoda_models import Product


class LamodaDao:
    def __init__(self, session: Depends(connect_db)):
        self.session = session
        self.db = session["lamoda"]

    def drop_collection(self):
        return self.db.drop()

    async def send_data(self, consumer: KafkaConsumer):
        products = self.db
        products_insert = []
        for message in consumer:
            products_insert.append(message.value)
        products.insert_many(products_insert)

    def create(self, product: Product = Body(...)) -> Dict[str, str]:
        encoded_product = jsonable_encoder(product)
        new_product = self.db.insert_one(encoded_product)
        return {"_id": str(new_product.inserted_id), **product.dict()}

    def get_elements(self):
        products = []
        for product in self.db.find():
            products.append(product)
        return paginate(products)

    def get_elements_by_category(self, category):
        products = []
        for product in self.db.find({"category": category}):
            products.append(product)
        return paginate(products)

    def get_element(self, _id: str):
        if len(_id) != 24:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid id value. Please, enter a 12-byte value",
            )
        element = self.db.find_one({"_id": ObjectId(_id)})
        if element is not None:
            element["_id"] = str(element["_id"])
            return element
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thing with ID {_id} not found",
            )

    def delete_element(self, _id):
        data = self.db.find_one({"_id": ObjectId(_id)})
        if data is not None:
            self.db.delete_one({"_id": ObjectId(_id)})
            return {"message": f"Item with ID {_id} was deleted"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thing with ID {_id} not found",
            )
