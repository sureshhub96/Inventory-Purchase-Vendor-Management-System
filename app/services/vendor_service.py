from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.vendor import Vendor
from app.schemas.vendor_schema import (
    VendorCreate,
    VendorUpdate
)


def create_vendor(vendor: VendorCreate, db: Session):
    """
    Create a new vendor.
    """

    existing_vendor = db.query(Vendor).filter(
        Vendor.email == vendor.email,
        Vendor.is_deleted == False
    ).first()

    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor email already exists."
        )

    new_vendor = Vendor(
        vendor_name=vendor.vendor_name,
        email=vendor.email,
        phone=vendor.phone,
        address=vendor.address,
        is_active=vendor.is_active
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor


def get_all_vendors(db: Session):
    """
    Get all active vendors.
    """

    return db.query(Vendor).filter(
        Vendor.is_deleted == False
    ).all()


def get_vendor(vendor_id: int, db: Session):
    """
    Get vendor by ID.
    """

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found."
        )

    return vendor


def update_vendor(
    vendor_id: int,
    vendor: VendorUpdate,
    db: Session
):
    """
    Update vendor.
    """

    existing_vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found."
        )

    email_exists = db.query(Vendor).filter(
        Vendor.email == vendor.email,
        Vendor.id != vendor_id,
        Vendor.is_deleted == False
    ).first()

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor email already exists."
        )

    existing_vendor.vendor_name = vendor.vendor_name
    existing_vendor.email = vendor.email
    existing_vendor.phone = vendor.phone
    existing_vendor.address = vendor.address
    existing_vendor.is_active = vendor.is_active

    db.commit()
    db.refresh(existing_vendor)

    return existing_vendor


def delete_vendor(
    vendor_id: int,
    db: Session
):
    """
    Soft delete vendor.
    """

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found."
        )

    vendor.is_deleted = True

    db.commit()

    return {
        "message": "Vendor deleted successfully."
    }