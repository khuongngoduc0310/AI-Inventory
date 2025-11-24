from fastapi import APIRouter
from app.utils.auth import get_current_user
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.crud import create_product, get_products
from fastapi import Depends
from app.services.forecast import forecast_demand
from fastapi import HTTPException



router = APIRouter()
@router.post("/products", response_model=ProductResponse)
def create_product_protected(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_product(db, product)

@router.get("/products", response_model=list[ProductResponse])
def read_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_products(db)

@router.get("/forecast/{product_id}")
def get_forecast(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    from app.models.product import Product
    if not db.query(Product).filter(Product.id == product_id).first():
        raise HTTPException(status_code=404, detail="Product not found")
    return forecast_demand(db, product_id)