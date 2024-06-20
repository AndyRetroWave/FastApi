import pytest
from app.bookings.dao import BookingDAO
from app.users.dao import UsersDAO
from app.bookings.models import Bookings


@pytest.mark.parametrize("id,email,is_present", [
    (1, "fedor@moloko.ru", True),
    (2, "....", False),
])
async def test_find_user_by_id(id, email, is_present):
    user = await UsersDAO.find_by_id(id)
    if is_present:
        assert user
        assert user.id == id
        assert user.email == email

    else:
        assert user.email != email


@pytest.mark.parametrize("id, date_to, date_from, is_present", [
    (2, "2023-03-23", "2023-03-13", True)])
async def test_get_bookings(id, date_to, date_from, is_present):
    booking = await BookingDAO.find_all(room_id=id)
    if is_present:
        for item in booking[0:2]:
            print(item['Bookings'].date_to)
            assert item['Bookings'].date_to.strftime('%Y-%m-%d') == date_to
            assert item['Bookings'].date_from.strftime('%Y-%m-%d') == date_from
    else:
        assert not booking
