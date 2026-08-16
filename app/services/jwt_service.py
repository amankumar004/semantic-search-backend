from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


class JWTService:

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )