from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt

from app.core.config import settings

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# Explicitly set Bcrypt as the hasher
password_hash = PasswordHash((BcryptHasher(),))




def get_password_hash(password: str) -> str:
    """Hashes a plain text password securely."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against its hash."""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT token containing payload data and expiration time."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt