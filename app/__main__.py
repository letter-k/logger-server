import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import click
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.models.base import session as _session
from app.models.users import UserCreate


@asynccontextmanager
async def session() -> AsyncGenerator[AsyncSession, None]:
    async for s in _session():
        yield s


@click.group(short_help="Комманды для работы с бд")
def db() -> None:
    pass


async def create_admin(email: str, password: str) -> None:
    await crud_user.create_user(
        session=session(),  # type: ignore
        user_create=UserCreate(
            email=email,
            is_active=True,
            is_superuser=True,
            password=password,
        ),
    )


@click.argument("email", type=str)
@click.argument("password", type=str)
@db.command(short_help="Создать админа")
def createsuperuser(email: str, password: str) -> None:
    asyncio.run(
        create_admin(
            email=email,
            password=password,
        )
    )
    click.echo("Админ создан")


if __name__ == "__main__":
    db()
