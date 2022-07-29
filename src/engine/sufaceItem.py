import pygame
from .object import Object
from .lib.vect import Vec2f


class SurfaceItem(Object):
    '''Surface item, base class for graphic present items'''
    surface: pygame.Surface
    size: pygame.Rect
    position: Vec2f
    visible: bool
    zIndex: int

    def __init__(self):
        super().__init__()
        self.surface = None
        self.size = pygame.Rect(0, 0, 0, 0)
        self.position = Vec2f()
        self.zIndex = 0
        self.visible = True

    def new(self, x: int, y: int):
        self.surface = pygame.Surface((x, y), pygame.SRCALPHA)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.x, self.position.y, self.size.w, self.size.h)

    def set_position(self, x: float, y: float):
        self.position.set(x, y)

    def surface_size(self) -> pygame.Rect:
        return self.surface.get_rect()

    def draw(self, surface: pygame.Surface):
        if self.visible:
            surface.blit(self.surface, self.position.to_tuple_int())
