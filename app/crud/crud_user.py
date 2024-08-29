from collections.abc import Callable
from typing import cast

from sqlmodel import insert, select

from app.api.deps import SessionDep
from app.core.security import get_password_hash, verify_password
from app.models.users import User, UserCreate, UserPublic


async def create_user(*, session: SessionDep, user_create: UserCreate) -> UserPublic:
    async with session as s:
        return UserPublic.model_validate(
            await s.scalar(
                insert(User)
                .values(
                    User.model_validate(
                        user_create,
                        update={
                            "hashed_password": get_password_hash(user_create.password)
                        },
                    ).model_dump()
                )
                .returning(User)
            )
        )


async def get_user_by_email(*, session: SessionDep, email: str) -> User | None:
    async with session as s:
        return (await s.exec(select(User).where(User.email == email))).one_or_none()


async def authenticate(
    *, session: SessionDep, email: str, password: str
) -> User | None:
    return (
        cast(
            Callable[[User | None], User | None],
            lambda user: (
                cast(
                    Callable[[User | None], User | None],
                    lambda user: (None, user)[
                        verify_password(password, cast(User, user).hashed_password)
                    ],
                ),
                cast(Callable[[User | None], None], lambda user: None),
            )[user is None](user),
        )
    )(await get_user_by_email(session=session, email=email))
