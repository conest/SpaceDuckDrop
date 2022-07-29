from __future__ import annotations
import pygame
from .sufaceItem import SurfaceItem
from .animation import Frame, AnimationGroup
from .lib import num
from .lib.vect import Vec2i


class Sprite(SurfaceItem):
    # Raw image data
    spritesheet: pygame.Surface

    # Number of Horizontal and Vertical frames
    _Hframes: int = 1
    _Vframes: int = 1

    # Frame number, useful for sprites sheets
    _max_frame: int = 1
    _frame: int = 1
    _frame_coords: Vec2i = Vec2i(0, 0)

    # Selected frame rect, use for draw on a surface
    _frame_rect: pygame.Rect
    _frame_rect_size: Vec2i = Vec2i(0, 0)

    # HACK: set offset and separation
    _frame_offset: Vec2i = Vec2i(0, 0)
    _frame_separation: Vec2i = Vec2i(0, 0)

    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.spritesheet = surface
        rect = self.spritesheet.get_rect()
        self._frame_rect = rect
        self._frame_rect_size = Vec2i(rect.w, rect.h)
        self.name = "Sprite"

    def new_from_img(imgPath: str) -> Sprite:
        '''For debuging'''
        img: pygame.Surface = pygame.image.load(imgPath)
        return Sprite(img)

    def draw(self, surface: pygame.Surface):
        '''(@Sprite) Overload SurfaceItem's draw method for better performance'''
        if self.visible:
            surface.blit(self.spritesheet, self.position.to_tuple_int(), self._frame_rect)

    def set_framesHV(self, h: int, v: int):
        '''Set horizontal and vertical numbers for the sprite sheet'''
        self._Hframes = max(1, h)
        self._Vframes = max(1, v)
        self._max_frame = self._Hframes * self._Vframes - 1
        rect_size_x = self.spritesheet.get_width() // self._Hframes
        rect_size_y = self.spritesheet.get_height() // self._Vframes
        self._frame_rect_size = Vec2i(rect_size_x, rect_size_y)
        self.size = pygame.Rect((0, 0), (rect_size_x, rect_size_y))

    def set_max_frame(self, max_frame: int):
        self._max_frame = max_frame

    def _set_frame_rect(self):
        '''Set frame rect according to the frame_coords'''
        x = self._frame_coords.x * self._frame_rect_size.x
        y = self._frame_coords.y * self._frame_rect_size.y
        self._frame_rect = pygame.Rect(x, y, self._frame_rect_size.x, self._frame_rect_size.y)

    def set_frame(self, frame: int):
        frame = min(frame, self._max_frame)
        self._frame = frame
        coords_y: int = frame // self._Hframes
        coords_x: int = frame % self._Hframes
        self._frame_coords.set(coords_x, coords_y)
        self._set_frame_rect()

    def set_frame_coords(self, coords_x: int, coords_y: int):
        coords_x = num.clip(coords_x, 0, self._Hframes - 1)
        coords_y = num.clip(coords_y, 0, self._Vframes - 1)
        self._frame_coords.set(coords_x, coords_y)
        self._frame = coords_x + coords_y * self._Hframes
        self._set_frame_rect()

    def frame_rect(self) -> pygame.Rect:
        return self._frame_rect

    def frame_size(self) -> Vec2i:
        return self._frame_rect_size

    def _update_surface(self):
        '''[Abandoned]'''
        self.surface = pygame.Surface((self.size.w, self.size.h), pygame.SRCALPHA).convert_alpha()
        self.surface.blit(self.spritesheet, (0, 0), self._frame_rect)


class AnimatedSprite(Sprite):

    animation: AnimationGroup

    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self.name = "AnimatedSprite"
        self.animation = AnimationGroup()

    def rect_from_coords(self, x: int, y: int) -> pygame.Rect:
        x = num.clip(x, 0, self._Hframes - 1)
        y = num.clip(y, 0, self._Vframes - 1)
        rx = x * self._frame_rect_size.x
        ry = y * self._frame_rect_size.y
        return pygame.Rect(rx, ry, self._frame_rect_size.x, self._frame_rect_size.y)

    def rect_from_frame(self, frame: int) -> pygame.Rect:
        frame = min(frame, self._max_frame)
        y: int = frame // self._Hframes
        x: int = frame % self._Hframes
        return self.rect_from_coords(x, y)

    def animation_bunch_frame_load(self, name: str, frames: list):
        '''frames is a list of Tuple: (coord_x, coord_y, duration)'''
        assert(self.animation.check(name)), f"No animation named {name}"
        for fTuple in frames:
            coord_x: int = fTuple[0]
            coord_y: int = fTuple[1]
            duration: int = fTuple[2]
            if len(fTuple) == 4:
                loopback: int = fTuple[3]
                frame = Frame(self.rect_from_coords(coord_x, coord_y), duration, loopback)
            else:
                frame = Frame(self.rect_from_coords(coord_x, coord_y), duration)
            self.animation.animations[name].add_frame(frame)

    def update(self, delta: int):
        '''(@AnimatedSprite) Overload SurfaceItem's update method for updating animation'''
        self.animation.update(delta)

    def draw(self, surface: pygame.Surface):
        '''(@AnimatedSprite) Overload SurfaceItem's draw method'''
        if self.visible:
            rect = self.animation.rect()
            surface.blit(self.spritesheet, self.position.to_tuple_int(), rect)
