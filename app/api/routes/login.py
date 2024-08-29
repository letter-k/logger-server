from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.core.security import Auth2PasswordRequest, Auth2RefreshToken
from app.crud import crud_user
from app.models.users import Token, User

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
    session: SessionDep, data: Annotated[Auth2PasswordRequest, Depends()]
) -> Token:
    user = await crud_user.authenticate(
        session=session, email=data.email, password=data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return Token(
        access_token=security.create_token(
            user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        refresh_token=security.create_token(
            f"refresh{user.id}refresh",
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        ),
    )


@router.post("/login/refresh-token")
async def login_refresh_token(
    session: SessionDep, data: Annotated[Auth2RefreshToken, Depends()]
) -> Token:
    token_data = security.decode_token(data.refresh_token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await session.get(User, f"{token_data.sub}".replace("refresh", ""))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return Token(
        access_token=security.create_token(
            user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        refresh_token=security.create_token(
            f"refresh{user.id}refresh",
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        ),
    )
