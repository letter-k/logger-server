from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), isolation_level="AUTOCOMMIT"
)
Session = async_sessionmaker(bind=engine, class_=AsyncSession)


class Base(SQLModel): ...


async def session() -> AsyncGenerator[AsyncSession, None]:
    """Обеспечивает транзакционную область для операций"""
    new_session = Session()
    try:
        yield new_session
    except Exception:
        await new_session.rollback()
        raise
    finally:
        await new_session.close()
