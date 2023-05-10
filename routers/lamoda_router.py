import asyncio

from dao.kafka_dao import KafkaSetup
from di.lamoda_di import LamodaService
from fastapi import APIRouter, Body, Depends
from fastapi_cache.decorator import cache
from fastapi_pagination import Page
from models.lamoda_models import Product
from parsers.lamoda_parser import LamodaParser

router = APIRouter(
    prefix="/lamoda",
    tags=["lamoda"],
)


@router.get("/products", response_model=Page[Product])
@cache()
def get_products(service: LamodaService = Depends()):
    return service.get_all_products()


@router.get("/products/{category}", response_model=Page[Product])
@cache()
def products_by_category(category: str, service: LamodaService = Depends()):
    return service.get_all_products_by_category(category)


@router.post("/create")
def create_product(product: Product = Body(...), service: LamodaService = Depends()):
    return service.create_product(product)


@router.delete("/products/{id}")
def delete_thing(_id: str, service: LamodaService = Depends()):
    return service.delete_product(_id)


@router.get("/products/{id}", response_model=Product)
@cache()
def product_by_id(_id: str, service: LamodaService = Depends()):
    return service.get_one_product(_id)


@router.get("/parsing")
async def parsing(service: LamodaService = Depends()):
    kafka = KafkaSetup()
    asyncio.get_event_loop()
    tasks = [
        asyncio.create_task(LamodaParser(kafka, service).parse()),
    ]
    asyncio.gather(*tasks)
