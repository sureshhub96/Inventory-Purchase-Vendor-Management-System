from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.purchase_order_schema import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderResponse
)

from app.services.purchase_order_service import (
    create_purchase_order,
    get_all_purchase_orders,
    get_purchase_order,
    update_purchase_order,
    purchase_history_by_vendor
)

from app.dependencies import admin_or_manager

router = APIRouter()


@router.post(
    "/",
    response_model=PurchaseOrderResponse,
    status_code=201,
    dependencies=[Depends(admin_or_manager)]
)
def create_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create Purchase Order
    """
    return create_purchase_order(order, db)


@router.get(
    "/",
    response_model=List[PurchaseOrderResponse],
    dependencies=[Depends(admin_or_manager)]
)
def read_orders(
    status: Optional[str] = Query(None),
    product_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """
    Get all purchase orders.

    Supports:
    - Status filter
    - Product search
    - Pagination
    """

    return get_all_purchase_orders(
        db=db,
        status_filter=status,
        product_name=product_name,
        page=page,
        limit=limit
    )


@router.get(
    "/{order_id}",
    response_model=PurchaseOrderResponse,
    dependencies=[Depends(admin_or_manager)]
)
def read_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get Purchase Order by ID
    """

    return get_purchase_order(order_id, db)


@router.put(
    "/{order_id}",
    response_model=PurchaseOrderResponse,
    dependencies=[Depends(admin_or_manager)]
)
def edit_order(
    order_id: int,
    order: PurchaseOrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update Purchase Order
    """

    return update_purchase_order(
        order_id,
        order,
        db
    )


@router.get(
    "/vendor/{vendor_id}",
    response_model=List[PurchaseOrderResponse],
    dependencies=[Depends(admin_or_manager)]
)
def vendor_purchase_history(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Purchase history by vendor.
    """

    return purchase_history_by_vendor(
        vendor_id,
        db
    )