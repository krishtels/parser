from typing import Dict

from config.database import connect_db
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder
from models.twitch_models import Stream

from dao.service_dao import ServiceDao


class TwitchDao(ServiceDao):
    def __init__(self, session: Depends(connect_db)):
        self.session = session
        self.db = session["twitch"]

    def create(self, stream: Stream = Body(...)) -> Dict[str, str]:
        encoded_stream = jsonable_encoder(stream)
        new_stream = self.db.insert_one(encoded_stream)
        return {"_id": str(new_stream.inserted_id), **stream.dict()}
