from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    sku: str
    stock_quantity: int = 0
    price: float

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True