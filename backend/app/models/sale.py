from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.models.base import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    unit_price = Column(Float, nullable=False)