import json
from datetime import date
from fastapi_versioning import version

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from app.bookings.dao import BookingDAO
from app.exception import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("/room")
@version(1)
async def get_bookings(room_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(room_id=room_id)


@router.post("/add.booking")
@version(1)
async def add_booking(
    background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    try:

        bookings = await BookingDAO.add(user.id, room_id, date_from, date_to)
        if not bookings:
            raise RoomCannotBeBooked
        else:
            booking_dict = bookings.to_dict()
            background_tasks.add_task(
                send_booking_confirmation_email, booking_dict, user.email)
            return bookings
    except:
        ...


@router.delete("/delete/{booking_id}")
@version(1)
async def delete_bookings(booking_id: int,
                          user: Users = Depends(get_current_user)):
    result = await BookingDAO.delete(booking_id, user.id)
    return {"succes": result}


@router.get("/add/bookings/{user_path}")
@version(1)
async def add_bookings_user_path(user_path: Users = Depends(get_current_user)):
    # Здесь user_path - это объект пользователя из пути маршрута
    result = await BookingDAO.get_booking_user(user_path.id)
    return result


@router.get("/id")
@version(1)
async def add_bookings_user_path(id: int, user_path:
                                 Users = Depends(get_current_user)):
    # Здесь user_path - это объект пользователя из пути маршрута
    result = await BookingDAO.get_bookings_id(user_path.id, id)
    return result
