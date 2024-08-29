from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Body
from passlib.context import CryptContext
from pydantic import EmailStr, ValidationError
from typing_extensions import Doc

from app.core.config import settings
from app.models.users import TokenPayload

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


ALGORITHM = "HS256"


def create_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)

    except (jwt.InvalidTokenError, ValidationError):
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class Auth2PasswordRequest:
    """
    ## Example

    ```python
    from typing import Annotated

    from fastapi import Depends, FastAPI
    from app.core.security import Auth2PasswordRequest

    app = FastAPI()


    @app.post("/login")
    def login(form_data: Annotated[Auth2PasswordRequest, Depends()]):
        data = {}

        if form_data.email:
            data["email"] = form_data.email
        return data
    ```
    """

    def __init__(
        self,
        *,
        email: Annotated[
            EmailStr,
            Body(),
            Doc(
                """
                `email` string.
                """
            ),
        ],
        password: Annotated[
            str,
            Body(),
            Doc(
                """
                `password` string.
                """
            ),
        ],
    ):
        self.email = email
        self.password = password


class Auth2RefreshToken:
    """
    ## Example

    ```python
    from typing import Annotated

    from fastapi import Depends, FastAPI
    from app.core.security import Auth2RefreshToken

    app = FastAPI()

    @app.post("/refresh-token")
    def refresh_token(form_data: Annotated[Auth2RefreshToken, Depends()]):
        return {"refresh_token": form_data.refresh_token}
    ```
    """

    def __init__(
        self,
        *,
        refresh_token: Annotated[
            str,
            Body(),
            Doc(
                """
                `refresh_token` string.
                """
            ),
        ],
    ):
        self.refresh_token = refresh_token
