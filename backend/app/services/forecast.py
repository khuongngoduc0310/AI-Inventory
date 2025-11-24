import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.sale import Sale

def get_sales_df(db: Session, product_id: int, days: int = 60):
    rows = db.query(Sale).filter(
        Sale.product_id == product_id,
        Sale.sale_date >= datetime.utcnow() - timedelta(days=days)
    ).all()
    df = pd.DataFrame([{"ds": r.sale_date, "y": r.quantity} for r in rows])
    return df.groupby("ds", as_index=False)["y"].sum()

def forecast_demand(db: Session, product_id: int, days_ahead: int = 14):
    df = get_sales_df(db, product_id)
    if len(df) < 2:
        return {"warning": "Not enough data", "predictions": []}
    
    model = Prophet(daily_seasonality=False, yearly_seasonality=False)
    model.fit(df)
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    
    future_df = forecast[["ds", "yhat"]].tail(days_ahead)
    predictions = [
        {"date": row["ds"].strftime("%Y-%m-%d"), "predicted_qty": round(row["yhat"], 2)}
        for _, row in future_df.iterrows()
    ]
    
    # Current stock
    from app.models.product import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    total_pred = sum(p["predicted_qty"] for p in predictions)
    
    return {
        "product_id": product_id,
        "current_stock": product.stock_quantity if product else 0,
        "total_forecast_14d": round(total_pred, 2),
        "predictions": predictions,
        "stockout_risk": total_pred > product.stock_quantity if product else True
    }