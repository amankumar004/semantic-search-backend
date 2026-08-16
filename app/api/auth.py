from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserRegister, UserRead, LoginRequest, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    return auth_service.register(
        email=request.email,
        password=request.password
    )

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    return auth_service.login(
        email=request.email,
        password=request.password
    )