from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    category: str
    brand: str
    name: str
    price: Decimal = Field(..., gt=0.0)
    description: Optional[dict]
    created: date = Field(default_factory=datetime.today)
