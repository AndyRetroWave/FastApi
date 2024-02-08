from ast import Dict

from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship


from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(
        Integer, Computed("(date_to - date_from) * price"), nullable=True
    )
    total_days = Column(Integer, Computed("date_to - date_from"), nullable=True)

    def to_dict(self) -> Dict:
        return {
            "room_id": self.room_id,
            "date_from": str(self.date_from),
            "date_to": str(self.date_to),
        }

    # user = relationship("Users", back_populates="booking")
    # room = relationship("Room", back_populates="booking")

    # def __str__(self):
    #     return f"Booking #{self.id}"
