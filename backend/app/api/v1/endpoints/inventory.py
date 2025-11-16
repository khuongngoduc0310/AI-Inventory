from fastapi import APIRouter
from app.utils.auth import get_current_user
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.crud import create_product, get_products
from fastapi import Depends



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