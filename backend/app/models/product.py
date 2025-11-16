# backend/app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sku = Column(String(50), unique=True, index=True)
    stock_quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)