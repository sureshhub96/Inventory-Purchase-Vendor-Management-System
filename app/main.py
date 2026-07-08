from fastapi import FastAPI

from app.database import Base, engine

# Import models so SQLAlchemy creates the tables
from app.models.user import User
from app.models.vendor import Vendor
from app.models.purchase_order import PurchaseOrder

# Import routers
from app.routers.auth_router import router as auth_router
from app.routers.vendor_router import router as vendor_router
from app.routers.purchase_order_router import (
    router as purchase_order_router
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Purchase & Vendor Management System",
    version="1.0.0",
    description="FastAPI Backend Application for Inventory Purchase & Vendor Management"
)

# Home Route
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Inventory Purchase & Vendor Management System",
        "status": "Running"
    }


# Authentication Routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Vendor Routes
app.include_router(
    vendor_router,
    prefix="/vendors",
    tags=["Vendor Management"]
)

# Purchase Order Routes
app.include_router(
    purchase_order_router,
    prefix="/purchase-orders",
    tags=["Purchase Order Management"]
)