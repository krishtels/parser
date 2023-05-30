import asyncio

from dao.kafka_dao import KafkaSetup
from di.twitch_di import TwitchService
from fastapi import APIRouter, Body, Depends
from fastapi_cache.decorator import cache
from fastapi_pagination import Page
from models.twitch_models import Stream
from parsers.twitch_parser import TwitchParser

router = APIRouter(
    prefix="/twitch",
    tags=["twitch"],
)


@router.get("/streams", response_model=Page[Stream])
@cache()
def get_products(service: TwitchService = Depends()):
    return service.get_all_products()


@router.post("/create")
def create_product(stream: Stream = Body(...), service: TwitchService = Depends()):
    return service.create_product(stream)


@router.delete("/streams/{id}")
def delete_thing(_id: str, service: TwitchService = Depends()):
    return service.delete_product(_id)


@router.get("/streams/{id}", response_model=Stream)
@cache()
def product_by_id(_id: str, service: TwitchService = Depends()):
    return service.get_one_product(_id)


@router.get("/parsing")
async def parsing(service: TwitchService = Depends()):
    kafka = KafkaSetup()
    asyncio.get_event_loop()
    tasks = [
        asyncio.create_task(TwitchParser(kafka, service).get_streams()),
    ]
    asyncio.gather(*tasks)
