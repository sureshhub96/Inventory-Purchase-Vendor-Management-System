from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    product_name: str

    quantity: int = Field(..., gt=0)

    unit_price: float = Field(..., gt=0)

    expected_delivery_date: date


class PurchaseOrderUpdate(BaseModel):
    product_name: str

    quantity: int = Field(..., gt=0)

    unit_price: float = Field(..., gt=0)

    expected_delivery_date: date

    status: str


class PurchaseOrderResponse(BaseModel):
    id: int
    vendor_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    expected_delivery_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)