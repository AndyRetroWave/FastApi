from sqlalchemy import insert, select

from app.bookings.models import Bookings
from app.database import async_session_maker


class BaseDAO:
    model = Bookings()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def post(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, model_id: int, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(
                id=model_id,
                user_id=user_id)
            result = await session.execute(query)
            obj_to_delete = result.scalar_one_or_none()
            if obj_to_delete:
                await session.delete(obj_to_delete)
                await session.commit()
