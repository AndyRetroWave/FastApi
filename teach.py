from typing import Any


class Circle:
    type_data = {
        "x": int,
        "y": int,
        "y": int
    }

    def __init__(self, x: int, y: int, radius: int):
        self.__x = x
        self.__y = y
        self.__radius = radius

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        self.__radius = radius

    def __setattr__(self, name: str, value: Any) -> None:
        if name in Circle.type_data and not isinstance(value, (Circle.type_data[name])):
            raise TypeError("Не правильный тип данных")
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        if not name in Circle.type_data:
            return False
        super().__getattribute__(name)


circle = Circle(10.5, '4', 22)
# прежнее значение не должно меняться, т.к. отрицательный радиус недопустим
circle.radius = -10
x, y = circle.x, circle.y
res = circle.name  # False, т.к. атрибут name не существует
