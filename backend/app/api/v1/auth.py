from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.db.redis import get_redis
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead
from app.repositories.user_repository import user_repo
from app.api.deps import get_current_user
from redis.asyncio import Redis

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_repo.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(
            user.id, expires_delta=refresh_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis)
) -> Any:
    """
    Refresh an access token using a refresh token
    """
    is_blacklisted = await redis_client.get(f"blocklist:{refresh_token}")
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    payload = security.verify_token(refresh_token, token_type="refresh")
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    user = await user_repo.get(db, id=user_id_str)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    # Optional: Rotate refresh token by blocklisting the old one
    await redis_client.setex(
        f"blocklist:{refresh_token}", 
        settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, 
        "true"
    )
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(
            user.id, expires_delta=refresh_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/logout")
async def logout(
    current_user = Depends(get_current_user),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")),
    redis_client: Redis = Depends(get_redis)
) -> Any:
    """
    Logout user by blocklisting their current access token
    """
    await redis_client.setex(
        f"blocklist:{token}", 
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, 
        "true"
    )
    return {"msg": "Successfully logged out"}

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user = await user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_repo.create(db, obj_in=user_in)
    return user
