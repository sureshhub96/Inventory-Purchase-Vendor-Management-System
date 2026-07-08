from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import UserRegister, Token
from app.schemas.user_schema import UserResponse
from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register User
    First Admin can register without authentication.
    """
    return register_user(user, db)


@router.post(
    "/login",
    response_model=Token
)
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(request, db)