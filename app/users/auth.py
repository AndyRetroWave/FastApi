from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import setting
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verefy_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expire_int: int, type_token: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_int)
    to_encode.update({
        "type": type_token,
        "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.SECRET_KEY, setting.ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict) -> str:
    access_token = create_token(data=data,
                                expire_int=setting.ACCESS_TOKEN_TIME_MINUTE,
                                type_token="access"
                                )
    return access_token


def create_refresh_token(date: dict = []) -> str:
    refresh_token = create_token(
        data=date, 
        expire_int=setting.REFRESH_TOKEN_TIME_MINUTE, 
        type_token="refresh"
        )
    return refresh_token


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_scalar(email=email)
    if not user or not verefy_password(password, user.hashed_password):
        return None
    return user
