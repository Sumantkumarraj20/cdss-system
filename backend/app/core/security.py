from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from jose import jwt, JWTError

SECRET_KEY = os.getenv("CDSS_JWT_SECRET", "change-me")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = int(os.getenv("CDSS_ACCESS_EXPIRE_MINUTES", "30"))
REFRESH_EXPIRE_MINUTES = int(os.getenv("CDSS_REFRESH_EXPIRE_MINUTES", "43200"))  # 30 days


def create_token(sub: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(sub: str) -> str:
    return create_token(sub, timedelta(minutes=ACCESS_EXPIRE_MINUTES))


def create_refresh_token(sub: str) -> str:
    return create_token(sub, timedelta(minutes=REFRESH_EXPIRE_MINUTES))


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
