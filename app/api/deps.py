from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security
from app.models.base import session
from app.models.users import User, UserInfo

SessionDep = Annotated[AsyncSession, Depends(session)]
TokenDep = Annotated[str, Depends(APIKeyHeader(name="Authorization"))]


async def get_current_user(*, session: SessionDep, token: TokenDep) -> UserInfo:
    token_data = security.decode_token(token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await session.get(User, token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return UserInfo.model_validate(user)


CurrentUser = Annotated[UserInfo, Depends(get_current_user)]


async def get_current_active_superuser(*, current_user: CurrentUser) -> UserInfo:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
