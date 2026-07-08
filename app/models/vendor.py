from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)

    vendor_name = Column(String(150), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    phone = Column(String(20), nullable=False)

    address = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    is_deleted = Column(Boolean, default=False)

    purchase_orders = relationship(
        "PurchaseOrder",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )