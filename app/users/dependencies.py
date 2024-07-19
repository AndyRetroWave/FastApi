from typing import Any
import uuid

from fastapi import Depends, Request, Response, status
from jose import JWTError, jwt

from app.config import setting
from app.exception import (AdminAccessExpireException,
                           TokenAsentException, TokenRefreshAsentException
                           )
from app.users.auth import create_token, valid__refresh_token
from app.users.dao import UsersDAO
from app.users.models import Users
from app.config import setting


def get_token_request(token_type: str):
    def dependency(request: Request):
        token = request.cookies.get(f"booking_{token_type}_token")
        if not token:
            raise TokenAsentException
        return token
    return dependency


async def get_current_user(response: Response,
                           token_access: str = Depends(
                               get_token_request("access")),
                           token_refresh: str = Depends(
                               get_token_request("refresh"))
                           ):
    try:
        try:
            payload = jwt.decode(
                token_access, setting.SECRET_KEY, setting.ALGORITHM
            )
            return await UsersDAO.get_users_email(payload.get('email'))
        except:
            valid_token_refresh = await valid__refresh_token(token_refresh)
            payload_access_no_valid = jwt.decode(
                token_access, setting.SECRET_KEY, setting.ALGORITHM,
                options={'verify_exp': False}
            )
            if token_refresh == await UsersDAO.\
                    get_refresh_token(payload_access_no_valid.get('email')) and\
                    not valid_token_refresh:
                email = payload_access_no_valid.get('email')
                access_token = create_token({
                    "sub": str(payload_access_no_valid.get('sub')),
                    "email": str(email),
                    "jti": str(uuid.uuid4()),
                },
                    setting.ACCESS_TOKEN_TIME_MINUTE,
                    "access")
                response.set_cookie("booking_access_token",
                                    access_token,
                                    httponly=True,
                                    expires=setting.ACCESS_TOKEN_TIME_MINUTE,
                                    )
                return await UsersDAO.get_users_email(email)
            else:
                raise TokenRefreshAsentException
    except JWTError:
        raise TokenAsentException


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise AdminAccessExpireException
    return current_user
