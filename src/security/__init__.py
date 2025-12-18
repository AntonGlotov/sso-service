from queries import get_user_hashed_password
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta
import jwt
from config import settings
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
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
    exp = datetime.now(timezone.utc) + expire
    payload = token_data
    payload.update({
        "exp": exp,
        "iat": datetime.now(timezone.utc)
    })

    return jwt.encode(
        payload=payload,
        key=get_private_key(),
        algorithm=settings.ALGORITHM
    )


def create_access_token(user: User) -> str:
    token_data = {
        "sub": user.username,
        "type": settings.ACCESS_TOKEN_TYPE
    }

    return create_jwt(
        token_data,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user: User) -> str:
    token_data = {
        "sub": user.username,
        "type": settings.REFRESH_TOKEN_TYPE
    }

    return create_jwt(
        token_data,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            get_public_key(),
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)

    if payload.get("type") != settings.ACCESS_TOKEN_TYPE:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_hashed_password(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_from_refresh_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_token(token)

    if payload.get("type") != settings.REFRESH_TOKEN_TYPE:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_hashed_password(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_from_refresh(
        current_user: Annotated[User, Depends(get_current_user_from_refresh_token)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")