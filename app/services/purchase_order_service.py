from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import or_

from app.models.purchase_order import PurchaseOrder
from app.models.vendor import Vendor

from app.schemas.purchase_order_schema import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate
)


def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session
):
    """
    Create Purchase Order
    """

    vendor = db.query(Vendor).filter(
        Vendor.id == order.vendor_id,
        Vendor.is_deleted == False
    ).first()

    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found."
        )

    if vendor.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create purchase order for inactive vendor."
        )

    total_amount = order.quantity * order.unit_price

    new_order = PurchaseOrder(
        vendor_id=order.vendor_id,
        product_name=order.product_name,
        quantity=order.quantity,
        unit_price=order.unit_price,
        total_amount=total_amount,
        expected_delivery_date=order.expected_delivery_date,
        status="Pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_all_purchase_orders(
    db: Session,
    status_filter: str = None,
    product_name: str = None,
    page: int = 1,
    limit: int = 10
):
    """
    Get Purchase Orders
    Supports:
    - Status Filter
    - Product Search
    - Pagination
    """

    query = db.query(PurchaseOrder)

    if status_filter:
        query = query.filter(
            PurchaseOrder.status == status_filter
        )

    if product_name:
        query = query.filter(
            PurchaseOrder.product_name.ilike(
                f"%{product_name}%"
            )
        )

    orders = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return orders


def get_purchase_order(
    order_id: int,
    db: Session
):
    """
    Get Purchase Order by ID
    """

    order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase Order not found."
        )

    return order

def update_purchase_order(
    order_id: int,
    order: PurchaseOrderUpdate,
    db: Session
):
    """
    Update Purchase Order
    """

    existing_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if existing_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found."
        )

    # Business Rule:
    # Received orders cannot be edited.
    if existing_order.status == "Received":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received purchase orders cannot be edited."
        )

    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0."
        )

    if order.unit_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit price must be greater than 0."
        )

    existing_order.product_name = order.product_name
    existing_order.quantity = order.quantity
    existing_order.unit_price = order.unit_price
    existing_order.expected_delivery_date = (
        order.expected_delivery_date
    )
    existing_order.status = order.status

    # Automatically recalculate total amount
    existing_order.total_amount = (
        order.quantity * order.unit_price
    )

    db.commit()
    db.refresh(existing_order)

    return existing_order


def purchase_history_by_vendor(
    vendor_id: int,
    db: Session
):
    """
    Get all purchase orders for a vendor.
    """

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found."
        )

    orders = db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id
    ).all()

    return orders