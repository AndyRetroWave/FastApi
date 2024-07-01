
from datetime import datetime
from typing import Any
import uuid

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt

from app.config import setting
from app.exception import (AdminAccessExpireException, IncorectTokenException,
                           TokenAsentException, TokenExpireException,
                           TokenRefreshAsentException, UserIsNotPresentException
                           )
from app.users.auth import create_access_token
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token_dependency(token: str):
    def get_token(request: Request):
        refresh_token = request.cookies.get(f"booking_{token}_token")
        if not refresh_token:
            raise TokenAsentException
        return refresh_token
    return get_token()


async def get_current_user(response: Response,
                           token_access: str = Depends(
                               get_token_dependency("access")),
                           token_refresh: str = Depends(
                               get_token_dependency("refresh"))
                           ):
    try:
        try:
            payload = jwt.decode(
                token_access, setting.SECRET_KEY, setting.ALGORITHM
            )
            email = await UsersDAO.get_users_email(payload.get('email'))
            return email
        except:
            payload_access_no_valid = jwt.decode(
                token_access, setting.SECRET_KEY, setting.ALGORITHM,
                options={'verify_exp': False}
            )
            if token_refresh == await UsersDAO.\
                    get_refresh_token(payload_access_no_valid.get('email')):
                sub = payload_access_no_valid.get('sub')
                email = payload_access_no_valid.get('email')
                jti_access = str(uuid.uuid4())
                access_token = create_access_token({
                    "sub": str(sub),
                    "email": str(email),
                    "jti": str(jti_access)
                })
                response.set_cookie("booking_access_token",
                                    access_token,
                                    httponly=True
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
