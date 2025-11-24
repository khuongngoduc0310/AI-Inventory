import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from random import randint
from app.core.database import SessionLocal
from app.models.product import Product
from app.models.sale import Sale

db = SessionLocal()

products = db.query(Product).all()
if not products:
    print("❌ Create a product first!")
    exit()

for p in products:
    for i in range(60):  # 60 days back
        date = datetime.utcnow().date() - timedelta(days=i)
        qty = randint(5, 15) if date.weekday() < 5 else randint(10, 25)  # Weekend spike
        sale = Sale(product_id=p.id, quantity=qty, sale_date=datetime.combine(date, datetime.min.time()), unit_price=p.price)
        db.add(sale)

db.commit()
print(f"✅ Seeded {60 * len(products)} sales rows")