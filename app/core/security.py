import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return str(pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def generate_api_key() -> tuple[str, str]:
    """Generates a raw API key and returns a tuple of (raw_key, hashed_key).

    The raw_key is shown to the user ONCE.
    The hashed_key is safely stored in PostgreSQL.
    """
    random_token = secrets.token_hex(32)
    raw_key = f"gw_live_{random_token}"
    hashed_key = hash_api_key(raw_key)
    return raw_key, hashed_key


def hash_api_key(raw_key: str) -> str:
    """Converts a raw API key into a deterministic SHA-256 hex string for database lookups."""
    clean_key = raw_key.strip()
    return hashlib.sha256(clean_key.encode("utf-8")).hexdigest()


def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:
    """Constructs a signed JWT token containing sub and exp claims."""
    now = datetime.now(UTC)

    expire = now + (expires_delta if expires_delta else timedelta(minutes=15))

    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # type: ignore[return-value]


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        return None
