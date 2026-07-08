from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.oauth2 import get_current_user
from app.models.user import User


def admin_only(
    current_user: User = Depends(get_current_user),
):
    """
    Allow only Admin users.
    """
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )

    return current_user


def manager_only(
    current_user: User = Depends(get_current_user),
):
    """
    Allow only Store Manager users.
    """
    if current_user.role != "Store Manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Store Manager access required."
        )

    return current_user


def admin_or_manager(
    current_user: User = Depends(get_current_user),
):
    """
    Allow both Admin and Store Manager.
    """
    if current_user.role not in ["Admin", "Store Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return current_user