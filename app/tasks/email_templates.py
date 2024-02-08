from email.message import EmailMessage

from pydantic import EmailStr

from app.config import setting


def create_booking_confirmarion_template(
    booking: dict,
    email_to: EmailStr,
    ):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"]= setting.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )
    return email