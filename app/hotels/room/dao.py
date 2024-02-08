from datetime import date

from sqlalchemy import String, and_, bindparam, func, join, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.room.models import Room

class RoomDAO(BaseDAO):
    model = Room
    
    @classmethod
    async def add_rooms(
        cls: int, 
        hotel_id: int,
        date_from: date,
        date_to: date
        ):
        """
        SELECT
            h.id,
            r.name AS room_name,
            h.name AS hotel_name,
            h.location,
            h.services,
            h.rooms_quantity,
            (r.quantity - COUNT(b.room_id)) AS available_rooms
        FROM
            hotels h
        JOIN
            rooms r ON h.id = r.hotel_id
        LEFT JOIN
            bookings b ON r.id = b.room_id AND (
                (b.date_from >= '2024-01-01' AND b.date_from <= '2024-01-24')
                OR (b.date_to >= '2024-01-01' AND b.date_from <= '2024-01-24')
                OR (b.date_to <= '2024-01-01' AND b.date_from > '2024-01-01')
            )
        WHERE
            r.hotel_id = 2
        GROUP BY
            r.quantity,
            b.room_id,
            h.id,
            r.hotel_id,
            r.name
        HAVING
            (r.quantity - COUNT(b.room_id)) != 0;
        """
        async with async_session_maker() as session:
            room_left = select(
                Room.id,
                Room.hotel_id.label('Hotel_id'),
                Room.name,
                Room.description,
                Room.services,
                Room.price,
                (Room.quantity - func.count(Bookings.room_id)).label("available_rooms")
                ).select_from(Hotels).join(Room, Room.hotel_id == Hotels.id).outerjoin(
                    Bookings, and_(
                        Room.id == Bookings.room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            ),
                            Bookings.id.is_(None)
                        )
                    )
                ).where(
                    Room.hotel_id == hotel_id
                ).group_by(
                    Room.id
                ).having(
                    (Room.quantity - func.count(Bookings.room_id)) != 0
                )
            hotel_left_result = await session.execute(room_left)
            return hotel_left_result.mappings().all()

