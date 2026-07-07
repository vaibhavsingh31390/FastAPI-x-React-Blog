from typing import Any
from jose import JWTError, jwt
from datetime import timedelta

from config.main_db import utc_now
from config.main_settings import SETTINGS


def create_jwt(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = utc_now() + timedelta(
        minutes=int(SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES or 30)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SETTINGS.SECRET_KEY,
        algorithm=SETTINGS.SECURITY_ALGO,
    )


def verify_jwt(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            SETTINGS.SECRET_KEY,
            algorithms=[SETTINGS.SECURITY_ALGO],
        )
        return payload
    except JWTError:
        return None
