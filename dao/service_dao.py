from abc import ABC

from bson import ObjectId
from config.database import connect_db
from fastapi import Depends, HTTPException, status
from fastapi_pagination import paginate
from kafka import KafkaConsumer


class ServiceDao(ABC):
    def __init__(self, session: Depends(connect_db)):
        self.session = session
        self.db = session["parser"]

    def drop_collection(self):
        return self.db.drop()

    async def send_data(self, consumer: KafkaConsumer):
        products = self.db
        products_insert = []
        for message in consumer:
            products_insert.append(message.value)
        products.insert_many(products_insert)

    def get_elements(self):
        products = []
        for product in self.db.find():
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
