from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from app.hotels.room.dao import RoomDAO
from app.hotels.room.schemas import SRoom

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"]
)


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms(
    hotel_id: int,
    date_from: date = Query(...,
                            description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(...,
                          description=f"Например, {datetime.now().date()}")
):
    room = await RoomDAO.add_rooms(hotel_id, date_from, date_to)
    room_json = parse_obj_as(List[SRoom], room)
    return room_json


@router.get("/get rooms all")
async def get_rooms_all():
    return await RoomDAO.post()
