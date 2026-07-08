from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.schemas.vendor_schema import (
    VendorCreate,
    VendorUpdate,
    VendorResponse
)

from app.services.vendor_service import (
    create_vendor,
    get_all_vendors,
    get_vendor,
    update_vendor,
    delete_vendor
)

from app.dependencies import admin_only

router = APIRouter()


@router.post(
    "/",
    response_model=VendorResponse,
    status_code=201,
    dependencies=[Depends(admin_only)]
)
def add_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):
    """
    Create Vendor
    Admin Only
    """
    return create_vendor(vendor, db)


@router.get(
    "/",
    response_model=List[VendorResponse],
    dependencies=[Depends(admin_only)]
)
def read_vendors(
    db: Session = Depends(get_db)
):
    """
    Get All Vendors
    """
    return get_all_vendors(db)


@router.get(
    "/{vendor_id}",
    response_model=VendorResponse,
    dependencies=[Depends(admin_only)]
)
def read_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get Vendor By ID
    """
    return get_vendor(vendor_id, db)


@router.put(
    "/{vendor_id}",
    response_model=VendorResponse,
    dependencies=[Depends(admin_only)]
)
def edit_vendor(
    vendor_id: int,
    vendor: VendorUpdate,
    db: Session = Depends(get_db)
):
    """
    Update Vendor
    """
    return update_vendor(vendor_id, vendor, db)


@router.delete(
    "/{vendor_id}",
    dependencies=[Depends(admin_only)]
)
def remove_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Soft Delete Vendor
    """
    return delete_vendor(vendor_id, db)