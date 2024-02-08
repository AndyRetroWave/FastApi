from fastapi import HTTPException, status


class BookingException(HTTPException): 
    status_code = 500 # <-- задаем значения по умолчанию
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"


class IncorrectUsernameOrPasswordException(BookingException): 
    status_code= status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль!"


class TokenExpireException(BookingException):  
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек!"


class TokenAsentException(BookingException): 
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутсвует"


class IncorectTokenException(BookingException): 
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


class UserIsNotPresentException(BookingException): 
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"


class DateFromMaxHotel(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Дата заезда должна быть раньше даты выезда"


class BookingMoreThan30Days(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Общее колличество дней привышает 30"