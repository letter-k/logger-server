import uuid

import sqlalchemy as sa
from sqlmodel import Field

from app.models.base import Base


class LogBase(Base):
    log_level: str = Field(sa_column=sa.Column(sa.String(255), nullable=False))
    message: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    extra_info: str = Field(sa_column=sa.Column(sa.Text, nullable=False))


class Log(LogBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: int | None = Field(
        default=None, foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
