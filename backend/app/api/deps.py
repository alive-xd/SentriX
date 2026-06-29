from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from uuid import UUID

from app.db.session import get_db
from app.db.redis import get_redis
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.models.organization import Organization
from app.repositories.user_repository import user_repo

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check blocklist
    is_blacklisted = await redis_client.get(f"blocklist:{token}")
    if is_blacklisted:
        raise credentials_exception

    payload = security.verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception
    
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    user = await user_repo.get_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active or current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_current_user_org(
    current_user: User = Depends(get_current_active_user),
) -> Optional[Organization]:
    """Returns the organization of the current user. Returns None if they don't have one."""
    return current_user.organization

class RequirePermissions:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    async def __call__(self, current_user: User = Depends(get_current_active_user)):
        if current_user.is_superuser:
            return current_user
        
        if not current_user.role_obj:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions (no role assigned)",
            )
            
        user_perms = set(current_user.role_obj.permissions)
        required_perms = set(self.required_permissions)
        
        if not required_perms.issubset(user_perms):
            missing = required_perms - user_perms
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Missing: {missing}",
            )
        
        return current_user
