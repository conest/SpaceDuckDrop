from __future__ import annotations


class Vec2i:
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.set(x, y)

    def __str__(self) -> str:
        return f'[Vec2i] (x: {self.x}, y: {self.y})'

    def set(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple:
        return (self.x, self.y)


class Vec2f:
    x: float = 0
    y: float = 0

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.set(x, y)

    def __str__(self) -> str:
        return f'[Vec2f] (x: {self.x}, y: {self.y})'

    def set(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def to_tuple_int(self) -> tuple:
        return (int(self.x), int(self.y))

    def __eq__(self, o) -> bool:
        if self.x == o.x and self.y == o.y:
            return True
        else:
            return False

    def __add__(self, o) -> Vec2f:
        return Vec2f(self.x + o.x, self.y + o.y)

    def __sub__(self, o) -> Vec2f:
        return Vec2f(self.x - o.x, self.y - o.y)

    def __mul__(self, o) -> Vec2f:
        return Vec2f(self.x * o, self.y * o)

    def __truediv__(self, o) -> Vec2f:
        return Vec2f(self.x / o, self.y / o)

    def __floordiv__(self, o) -> Vec2f:
        return Vec2f(self.x // o, self.y // o)

    def move(self, x, y) -> None:
        self.x += x
        self.y += y
