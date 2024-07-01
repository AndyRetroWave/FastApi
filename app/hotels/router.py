import asyncio
from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, FastAPI, Query, status
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from app.exception import BookingMoreThan30Days, DateFromMaxHotel
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel

app = FastAPI()

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=30)
async def get_hotels(
        location: str,
        date_from: date = Query(...,
            description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., 
            description=f"Например, {datetime.now().date()}")):
    # await asyncio.sleep(3)
    if date_from >= date_to:
        raise DateFromMaxHotel
    elif (date_to - date_from) > timedelta(days=30):
        raise BookingMoreThan30Days
    hotels = await HotelDAO.get_hotel(location, date_from, date_to)
    hotel_json = parse_obj_as(List[SHotel], hotels)
    return hotel_json


@router.get("/id/{hotels_id}")
async def get_hotels_one(hotels_id: int):
    return await HotelDAO.get_hotel_id(hotels_id)


@router.get("/get hotels all")
async def get_hotels_all():
    return await HotelDAO.post()


@router.post("/add hotel")
async def adds_hotel(
        name: str = Query(..., description=f"Наименование отеля"),
        location: str = Query(..., description=f"Местоположение отеля"),
        services: str = Query(...,
                              description=f"Предоставляемые услуги отеля"),
        rooms_quantity: int = Query(..., description=f"Кол-во комнат отеля"),
        image_id: int = Query(..., description=f"Номер картинки по отеля")):
    return await HotelDAO.add_hotels(name,
                                     location,
                                     services,
                                     rooms_quantity,
                                     image_id
                                     )

