from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.room.models import Room
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Bookings.id] 
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class RoomsAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c]
    name = "Комнаты"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] 
    name = "Отели"
    name_plural = "Отели"
    icon = "fa-solid fa-bed"
