from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product_by_sku(db: Session, sku: str):
    return db.query(Product).filter(Product.sku == sku).first()