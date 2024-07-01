from smtplib import SMTPException

from fastapi import APIRouter, Depends, Request, Response

from app.exception import (IncorrectRefreshTokenException, IncorrectUsernameOrPasswordException,
                           UserAlreadyExistsException)
from app.users.auth import (authenticate_user, create_access_token,
                            create_refresh_token, get_password_hash,
                            verefy_password, )
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
import uuid

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    print(user)
    if not user:
        raise IncorrectUsernameOrPasswordException
    access_token = create_access_token({
        "sub": str(user.id),
        "email": str(user.email),
        "jti": str(uuid.uuid4())
    })
    refresh_token = create_refresh_token({
        "jti": str(uuid.uuid4())
    })
    await UsersDAO.set_refresh_token(refresh_token, user_data)
    response.set_cookie("booking_access_token", access_token, httponly=True)
    response.set_cookie("booking_refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/update_refresh_token")
async def update_refresh_token(response: Response,
                               refresh: str,
                               email: str,
                               User=Depends(get_current_admin_user)):
    if refresh == await UsersDAO.get_refresh_token(email):
        refresh_token = create_refresh_token({
            "jti": str(uuid.uuid4())
        })
        refresh_str = str(refresh_token)
        await UsersDAO.set_refresh_token(refresh_token, email)
        response.set_cookie("booking_refresh_token",
                            refresh_token,
                            httponly=True
                            )
        return {"refresh": refresh_str}
    raise IncorrectRefreshTokenException


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    response.delete_cookie("booking_refresh_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.post()
