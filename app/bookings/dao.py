from datetime import date

from sqlalchemy import Engine, and_, func, insert, or_, select, AdaptedConnection

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.room.models import Room
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger



class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_to >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_to <= '2023-05-15' AND date_from > '2023-06-15')
        """
        async with async_session_maker() as session:
            msg = ""
            try:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                """        
                SELECT rooms.quantity - COUNT(bookings.room_id) FROM rooms
                LEFT JOIN bookings ON bookings.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, bookings.room_id
                """
                get_rooms_left = (
                    select(
                        Room.quantity
                        - func.count(booked_rooms.c.room_id).label("rooms_left"),
                    )
                    .select_from(Room)
                    .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )
                print(get_rooms_left.compile(engine, compile_kwargs={"loteral_binds":True}))


                rooms_left = await session.execute(get_rooms_left)
                rooms_left_fin = rooms_left.scalar()
                if rooms_left_fin > 0:
                    get_price = await session.execute(
                        select(Room.price).filter_by(id=room_id)
                    )
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=get_price.scalar(),
                        )
                        .returning(Bookings)
                    )
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                elif isinstance(e, SQLAlchemyError):
                    msg = "Unknown Exc"
                msg += ": Cannot add booking"
                extra = {
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to
                }
                logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def get_booking_user(cls, user_id: int):
        async with async_session_maker() as session:
            """
            SELECT b.room_id,
                b.user_id,
                b.date_from,
                b.date_to,
                b.price,
                b.total_cost,
                r.image_id,
                r.name,
                r.description,
                r.services
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.user_id = 4
            """
            get_booking = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Room.image_id,
                    Room.name,
                    Room.description,
                    Room.services,
                )
                .select_from(Bookings)
                .join(Room, Bookings.room_id == Room.id)
                .where(Bookings.user_id == user_id)
            )
            room_result = await session.execute(get_booking)
            await session.commit()
            return room_result.mappings().all()

    @classmethod
    async def get_bookings_id(cls, user_id: int, id: int):
        async with async_session_maker() as session:
            """
            SELECT b.room_id,
                b.user_id,
                b.date_from,
                b.date_to,
                b.price,
                b.total_cost,
                r.image_id,
                r.name,
                r.description,
                r.services
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.id = 4
            """
            get_booking_id = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Room.image_id,
                    Room.name,
                    Room.description,
                    Room.services,
                )
                .select_from(Bookings)
                .join(Room, Bookings.room_id == Room.id)
                .where(Bookings.id == id)
            )
            room_result = await session.execute(get_booking_id)
            await session.commit()
            return room_result.mappings().all()
    
    @classmethod
    async def find_all(cls, room_id):
        """
        SELECT * 
        FROM Booking
        WHERE booking.room_id = room_id
        """
        async with async_session_maker() as session:
            booking = select(cls.model).where(cls.model.room_id == room_id)
            result = await session.execute(booking)
            return result.mappings().all()