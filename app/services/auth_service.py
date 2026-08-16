from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRead, TokenResponse
from app.services.jwt_service import JWTService
from app.services.security_service import SecurityService


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.security_service = SecurityService()
        self.jwt_service = JWTService()

    def register(
        self,
        email: str,
        password: str
    ) -> UserRead:

        existing_user = self.user_repository.get_user_by_email(
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        password_hash = self.security_service.hash_password(
            password
        )

        user = User(
            email=email,
            password_hash=password_hash
        )

        created_user = self.user_repository.create_user(user)

        return UserRead.model_validate(created_user)

    def login(
        self,
        email: str,
        password: str
    ) -> TokenResponse:

        user = self.user_repository.get_user_by_email(
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        password_valid = self.security_service.verify_password(
            password,
            user.password_hash
        )

        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        access_token = self.jwt_service.create_access_token(
            user_id=user.id
        )

        return TokenResponse(
            access_token=access_token
        )