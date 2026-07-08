from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id"),
        nullable=False
    )

    product_name = Column(String(200), nullable=False)

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Float, nullable=False)

    total_amount = Column(Float, nullable=False)

    expected_delivery_date = Column(Date, nullable=False)

    status = Column(
        String(30),
        default="Pending"
    )

    vendor = relationship(
        "Vendor",
        back_populates="purchase_orders"
    )