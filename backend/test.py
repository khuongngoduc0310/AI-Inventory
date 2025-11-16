from app.core.database import engine, SessionLocal
from app.utils.crud import create_product
from app.schemas.product import ProductCreate
from app.models.base import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()
new_product = create_product(db, ProductCreate(
    name="Test Laptop", sku="LT-001", stock_quantity=15, price=999.99
))
print(new_product)