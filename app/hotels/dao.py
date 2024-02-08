import json
from datetime import date

from sqlalchemy import (JSON, String, and_, bindparam, func, insert, join, or_,
                        select)

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.room.models import Room


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotel(
        cls: int,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
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
                (b.date_from >= '2024-01-12' AND b.date_from <= '2024-01-24')
                OR (b.date_to >= '2024-01-12' AND b.date_from <= '2024-01-24')
                OR (b.date_to <= '2024-01-12' AND b.date_from > '2024-01-12')
                )
            WHERE
                h.location LIKE '%Алтай%'
            GROUP BY
                r.quantity,
                b.room_id,
                h.id,
                r.hotel_id,
                r.name
            HAVING
                (r.quantity - COUNT(b.room_id)) != 0;
            """
            hotel_left = select(
                Hotels.id,
                Room.name,
                Hotels.name.label('hotel_name'),
                Hotels.location,
                Hotels.services.label('services'),
                Hotels.rooms_quantity,
                Hotels.image_id,
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
                Hotels.location.like(f'%{location}%')
            ).group_by(
                Room.quantity,
                Bookings.room_id,
                Hotels.id,
                Room.hotel_id,
                Room.name
            ).having(
                (Room.quantity - func.count(Bookings.room_id)) != 0
            )

            hotel_left_result = await session.execute(hotel_left)
            print(hotel_left_result)
            return hotel_left_result.mappings().all()
        

    @classmethod
    async def get_hotel_id(cls, hotel_id: int):
        async with async_session_maker() as session:
            get_hotel = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id).select_from(Hotels).where(Hotels.id == hotel_id)
            add_hotel_result = await session.execute(get_hotel)
            return add_hotel_result.mappings().all()
        
    @classmethod
    async def add_hotels(cls, 
        name: str,
        location: str, 
        services: JSON,
        rooms_quantity: int,
        image_id: int):
        async with async_session_maker() as session:
            decoded_services = json.dumps(services).encode('utf-8').decode('unicode_escape')
            add_hotel = insert(Hotels).values(
                name=name,
                location=location,
                services=decoded_services,
                rooms_quantity=rooms_quantity, 
                image_id=image_id,
                ).returning(Hotels)
            print(add_hotel)
            adds_hotel = await session.execute(add_hotel)
            await session.commit()
            return adds_hotel.scalar()