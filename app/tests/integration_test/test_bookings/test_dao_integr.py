from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_bookings = await BookingDAO.add(
        user_id=4,
        room_id=2,
        date_from=datetime.strptime("2023-03-13", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-03-23", "%Y-%m-%d")
        )
    assert new_bookings.user_id == 4
    assert new_bookings.room_id == 2

    new_bookings = await BookingDAO.find_by_id(new_bookings.id)

    assert new_bookings is not None