from collections.abc import Sequence

from sqlmodel import select

from app.api.deps import SessionDep
from app.models.logs import Log, LogBase


async def cratea_log(
    *, session: SessionDep, log_create: LogBase, owner_id: int
) -> None:
    async with session as s:
        s.add(Log.model_validate(log_create, update={"owner_id": owner_id}))
        await s.commit()


async def logs_by_user(*, session: SessionDep, owner_id: int) -> Sequence[Log]:
    async with session as s:
        return (await s.exec(select(Log).where(Log.owner_id == owner_id))).all()
