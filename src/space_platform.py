import random
# from enum import Enum, auto
import pygame
from engine.lib.num import clip
from engine.lib.vect import Vec2f
from engine.sprite import Sprite
from engine.sufaceItem import SurfaceItem


class Platform:
    ZOOM: int = 2
    PIXEL_SIZE: int = 16 * ZOOM

    image: SurfaceItem
    spSheet: Sprite
    hitbox: pygame.Rect

    name: str
    position: Vec2f
    length: int

    def __init__(self, sheetSurface: pygame.Surface, ticks: int):
        name: str = "platform" + str(ticks) + str(random.randint(0, 100))
        self.image = SurfaceItem()
        self.image.name = self.name = name
        self.position = Vec2f()
        self.length = 0

        self.spSheet = Sprite(sheetSurface)
        self.spSheet.set_framesHV(5, 1)
        self.hitbox = pygame.Rect(0, 0, 0, 0)

    def generate(self, length: int):
        length = clip(length, 1, 20)
        self.length = length
        self.image.new(length * Platform.PIXEL_SIZE, Platform.PIXEL_SIZE)

        if length == 1:
            self.spSheet.set_frame(4)
            self.spSheet.draw(self.image.surface)
            return

        for i in range(length):
            if i == 0:
                self.spSheet.set_frame(0)
            elif i == length - 1:
                self.spSheet.set_frame(2)
            else:
                self.spSheet.set_frame(1)
            self.spSheet.position = Vec2f(Platform.PIXEL_SIZE * i, 0)
            self.spSheet.draw(self.image.surface)

    def _syn_position(self):
        self.image.position = self.position
        size = (Platform.PIXEL_SIZE * self.length, Platform.PIXEL_SIZE)
        self.hitbox = pygame.Rect(self.position.to_tuple_int(), size)

    def move_to(self, x: float, y: float):
        self.position.set(x, y)
        self._syn_position()

    def move(self, x: float, y: float):
        self.position.move(x, y)
        self._syn_position()
