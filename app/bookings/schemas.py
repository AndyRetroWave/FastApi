from datetime import date

from pydantic import BaseConfig, BaseModel


class SBooking(BaseModel):
    room_id: int
    user_id: int
    date_to: date
    id: int
    price: int
    total_days: int
    date_from: date
    total_cost: int

    class Config(BaseConfig):
        arbitrary_types_allowed = True
