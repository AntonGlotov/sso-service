from queries import get_user_hashed_password
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta
import jwt
from config import settings
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dto import TokenData, User
from pem_utils import get_private_key, get_public_key

password_hash = PasswordHash.recommended()

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user_hashed_password(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_jwt(token_data, expire):
    exp = datetime.now(timezone.utc) + timedelta(minutes=expire)
    payload = token_data
    payload.update({"exp": exp,
                    "iat": datetime.now(timezone.utc)
    })


    return jwt.encode(
        payload=payload,
        key=get_private_key(),
        algorithm=settings.ALGORITHM
    )


def create_access_token(user: User) -> str:
    token_data = {
        "type": settings.ACCESS_TOKEN_TYPE,
        "username": user.username
    }

    return create_jwt(
        token_data,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def create_refresh_token(user: User) -> str:
    token_data = {
        "type": settings.REFRESH_TOKEN_TYPE,
        "username": user.username
    }

    return create_jwt(
        token_data,
        settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_public_key(), algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user_hashed_password(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user