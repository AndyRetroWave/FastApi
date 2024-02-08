import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    *[(10, "2023-03-13", "2023-03-23", 200)]*6,
    (10, "2023-03-13", "2023-03-23", 409)
])
async def test_add_and_get_booking_api(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings/add.booking", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    print(response.iter_text)
    assert response.status_code == status_code



@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2023-03-13", "2023-03-23", 200),
    ("Алтай", "2023-03-24", "2023-03-23", 400),
    ("Алтай", "2023-03-12", "2023-04-23", 400)
])
async def test_get_hotel(location, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/hotels", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    (1, "2023-03-13", "2023-03-23", 200)
])
async def test_grud_booking_user(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings/add.booking", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    response_data = response.json