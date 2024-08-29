import sqlalchemy as sa
from pydantic import EmailStr
from sqlmodel import Field

from app.models.base import Base


class UserBase(Base):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(sa_column=sa.Column(sa.Boolean, default=True))
    is_superuser: bool = Field(sa_column=sa.Column(sa.Boolean, default=False))


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(Base):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int | None = Field(
        default=None, sa_column=sa.Column(sa.Integer, primary_key=True)
    )
    hashed_password: str = Field(max_length=255)


class UserInfo(UserBase):
    id: int
    hashed_password: str


class UserPublic(UserBase):
    id: int


class Token(Base):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(Base):
    sub: str | None = None
