from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker
from sqlalchemy import delete, select, update

from app.users.schemas import SUserAuth


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def set_refresh_token(cls, token: str, user):
        """
        INSERT INTO Users(refresh_jwt_token)
        VALUE("token")
        """
        async with async_session_maker() as session:
            if isinstance(user, SUserAuth):
                set_token = update(Users).where(Users.email == user.email)\
                    .values(refresh_jwt_token=token)
            else:
                set_token = update(Users).where(Users.email == user)\
                    .values(refresh_jwt_token=token)
            await session.execute(set_token)
            await session.commit()

    @classmethod
    async def get_refresh_token(csl, email: str) -> str:
        """
        SELECT refresh_jwt_token
        FROM Users
        """
        async with async_session_maker() as session:
            token = select(Users.refresh_jwt_token).where(Users.email == email)
            result = await session.execute(token)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_refresh_token(cls, email):
        """
        DELETE REFRESH TOKEN
        FROM USER
        WHERE email == email 
        """
        async with async_session_maker() as session:
            token = delete(cls.model.refresh_jwt_token).where(
                Users.email == email)
            await session.execute(token)
            await session.commit()

    @classmethod
    async def get_users_email(cls, email):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar()
