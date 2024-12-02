from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotFoundException,
)
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        # raise AuthenticationTokenAbsenceException
        return None
    else:
        return token


async def get_current_user(token: str | None = Depends(get_token)):

    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_JWT_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotFoundException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotFoundException

    return user
