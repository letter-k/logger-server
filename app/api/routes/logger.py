from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_user
from app.crud import crud_log
from app.models.logs import LogBase
from app.models.other import Message

router = APIRouter()


@router.post("/", dependencies=[Depends(get_current_user)], response_model=Message)
async def create_log(
    *, session: SessionDep, user: CurrentUser, log_create: LogBase
) -> Message:
    await crud_log.cratea_log(session=session, log_create=log_create, owner_id=user.id)
    return Message(message="log received")


@router.get("/", dependencies=[Depends(get_current_user)], response_model=list[LogBase])
async def logs(*, session: SessionDep, user: CurrentUser) -> Any:
    return await crud_log.logs_by_user(session=session, owner_id=user.id)
