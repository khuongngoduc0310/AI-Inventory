from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import auth, inventory
from app.core.database import engine
from app.models.base import Base
from app.models.sale import Sale

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")
    yield
    # Shutdown logic (optional)
    # e.g., close DB connections, cleanup tasks
    print("👋 Application shutting down...")

app = FastAPI(
    title="RetailIQ API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}