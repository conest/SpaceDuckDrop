import random
import pygame
from engine.animation import Animation
from engine.sprite import AnimatedSprite
from engine.lib.vect import Vec2f


class Background:
    ZOOM: int = 2

    sprite: AnimatedSprite

    def __init__(self, name: str, sheetSurface: pygame.Surface):
        self.name = name

        self.sprite = AnimatedSprite(sheetSurface)
        self.sprite.name = name
        self.sprite.set_framesHV(4, 1)
        self.sprite.zIndex = -1

        frames: list = [
            (0, 0, random.randint(1000, 2000)), (1, 0, random.randint(1000, 2000)),
            (2, 0, random.randint(1000, 2000)), (3, 0, random.randint(1000, 2000))]
        self.sprite.animation.add("idle", Animation(True))
        self.sprite.animation_bunch_frame_load("idle", frames)
        self.sprite.animation.play("idle")

    def move_to(self, x: float, y: float):
        self.sprite.position = Vec2f(x, y)
