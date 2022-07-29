from enum import Enum, auto
import pygame
from engine.lib.num import approach
from engine.lib.vect import Vec2f
from engine.resource import resource
from engine.sufaceItem import SurfaceItem
from engine.sprite import AnimatedSprite
from engine.animation import Animation


class Status(Enum):
    IDLE = auto()
    WALK = auto()
    FALLING = auto()


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


class Duck:
    NAME = "duck"
    ZOOM = 2
    PIXEL_SIZE: 32 * ZOOM
    ACCELERATION = 0.0004
    SPEED_H_LIMIT = 0.2
    RESISTANCE = 0.0006
    GRAVITY = 0.0003
    GRAVITY_LIMIT = 0.3

    HIT_SIZE = (28, 28)
    HIT_POS = (14, 36)

    sprite: AnimatedSprite
    position: Vec2f
    status: Status
    name: str

    hitbox: pygame.Rect
    visualizedHB: SurfaceItem
    debug: bool

    keepLeft: bool
    keepRight: bool
    direction: Direction
    speedH: float
    speedV: float
    moveTrend: Vec2f

    def __init__(self):
        # double size the duck
        resource.add_surface("duck", "assets/duck_dark.png")
        resource.scale_surface("duck", Duck.ZOOM)

        self.sprite = AnimatedSprite(resource.surface("duck"))
        self.sprite.name = Duck.NAME
        self.sprite.set_framesHV(15, 17)
        self._load_animation()

        self.position = Vec2f()
        self.status = Status.IDLE
        self.name = Duck.NAME

        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.visualizedHB = SurfaceItem()
        self.visualizedHB.name = "visualizedHB"
        self.visualizedHB.new(Duck.HIT_SIZE[0], Duck.HIT_SIZE[1])
        self.visualizedHB.surface.fill(pygame.Color(0, 0, 128, 128))

        self.keepLeft = False
        self.keepRight = False
        self.direction = Direction.RIGHT
        self.speedH = 0
        self.speedV = 0

    def __str__(self) -> str:
        size = self.sprite.frame_size()
        return f'[Duck] Frame Size: ({size.x}, {size.y})'

    def _load_animation(self):
        duck = self.sprite

        frames: list = [(2, 1, 300), (3, 1, 300)]
        duck.animation.add("idle_l", Animation(True))
        duck.animation_bunch_frame_load("idle_l", frames)

        frames: list = [(2, 0, 300), (3, 0, 300)]
        duck.animation.add("idle_r", Animation(True))
        duck.animation_bunch_frame_load("idle_r", frames)

        frames: list = [(0, 5, 150), (1, 5, 150), (2, 5, 150), (3, 5, 150)]
        duck.animation.add("walk_l", Animation(True))
        duck.animation_bunch_frame_load("walk_l", frames)

        frames: list = [(0, 6, 150), (1, 6, 150), (2, 6, 150), (3, 6, 150)]
        duck.animation.add("walk_r", Animation(True))
        duck.animation_bunch_frame_load("walk_r", frames)

        frames: list = [(0, 4, 100), (1, 4, 100), (2, 4, 100), (3, 4, 100)]
        duck.animation.add("turn_l", Animation(False))
        duck.animation_bunch_frame_load("turn_l", frames)

        frames: list = [(3, 4, 100), (2, 4, 100), (1, 4, 100), (0, 4, 100)]
        duck.animation.add("turn_r", Animation(False))
        duck.animation_bunch_frame_load("turn_r", frames)

        frames: list = [(5, 8, 100), (6, 8, 100), (7, 8, 100), (8, 8, 100)]
        duck.animation.add("turn_air_l", Animation(False))
        duck.animation_bunch_frame_load("turn_air_l", frames)

        frames: list = [(8, 8, 100), (7, 8, 100), (6, 8, 100), (5, 8, 100)]
        duck.animation.add("turn_air_r", Animation(False))
        duck.animation_bunch_frame_load("turn_air_r", frames)

        frames: list = [(5, 9, 100), (6, 9, 100), (7, 9, 100), (8, 9, 100), (9, 9, 100, 1)]
        duck.animation.add("fall_r", Animation(True))
        duck.animation_bunch_frame_load("fall_r", frames)

        frames: list = [(5, 10, 100), (6, 10, 100), (7, 10, 100), (8, 10, 100), (9, 10, 100, 1)]
        duck.animation.add("fall_l", Animation(True))
        duck.animation_bunch_frame_load("fall_l", frames)

        frames: list = [
            (5, 13, 200), (6, 13, 200), (7, 13, 200),
            (8, 13, 200), (9, 13, 200), (10, 13, 200)]
        duck.animation.add("sleep", Animation(True))
        duck.animation_bunch_frame_load("sleep", frames)

        frames: list = [
            (5, 13, 200), (4, 13, 200), (5, 13, 200), (4, 13, 400),
            (11, 13, 200), (12, 13, 200), (13, 13, 200), (14, 13, 200)]
        duck.animation.add("awake", Animation(False))
        duck.animation_bunch_frame_load("awake", frames)

        duck.animation.play("sleep")

    def _syn_position(self):
        self.sprite.position = self.position
        v2Pos = self.position + Vec2f(Duck.HIT_POS[0], Duck.HIT_POS[1])
        hitSize = (Duck.HIT_SIZE[0], Duck.HIT_SIZE[1])
        self.hitbox = pygame.Rect(v2Pos.to_tuple_int(), hitSize)
        self.visualizedHB.position = v2Pos

    def change_status(self, s: Status):
        self.status = s

    def des_hitbox(self) -> pygame.Rect:
        v2Pos = self.position + self.moveTrend + Vec2f(Duck.HIT_POS[0], Duck.HIT_POS[1])
        hitSize = (Duck.HIT_SIZE[0], Duck.HIT_SIZE[1])
        return pygame.Rect(v2Pos.to_tuple_int(), hitSize)

    def feet_hitbox(self) -> pygame.Rect:
        return self.hitbox.move(0, 1)

    def _turn_to(self, dir: Direction, falling: bool):
        self.direction = dir
        match (dir, falling):
            case (Direction.LEFT, False):
                self.sprite.animation.play("turn_l")
                self.sprite.animation.set_next("walk_l")
            case (Direction.RIGHT, False):
                self.sprite.animation.play("turn_r")
                self.sprite.animation.set_next("walk_r")
            case (Direction.LEFT, True):
                self.sprite.animation.play("turn_air_l")
                self.sprite.animation.set_next("fall_l", 1)
            case (Direction.RIGHT, True):
                self.sprite.animation.play("turn_air_r")
                self.sprite.animation.set_next("fall_r", 1)

    def go_left(self):
        self.keepLeft = True
        match self.status:
            case Status.WALK:
                if self.direction != Direction.LEFT:
                    self._turn_to(Direction.LEFT, False)
            case Status.FALLING:
                if self.direction != Direction.LEFT:
                    self._turn_to(Direction.LEFT, True)
            case _:
                self.change_status(Status.WALK)
                if self.direction != Direction.LEFT:
                    self._turn_to(Direction.LEFT, False)
                else:
                    self.sprite.animation.play("walk_l")

    def go_right(self):
        self.keepRight = True
        match self.status:
            case Status.WALK:
                if self.direction != Direction.RIGHT:
                    self._turn_to(Direction.RIGHT, False)
            case Status.FALLING:
                if self.direction != Direction.RIGHT:
                    self._turn_to(Direction.RIGHT, True)
            case _:
                self.change_status(Status.WALK)
                if self.direction != Direction.RIGHT:
                    self._turn_to(Direction.RIGHT, False)
                else:
                    self.sprite.animation.play("walk_r")

    def release_left(self):
        self.keepLeft = False
        if not self.keepRight:
            return
        match self.status:
            case Status.WALK:
                if self.direction == Direction.LEFT:
                    self._turn_to(Direction.RIGHT, False)
            case Status.FALLING:
                self._turn_to(Direction.RIGHT, True)
            case Status.IDLE:
                self.direction = Direction.RIGHT
                self.sprite.animation.play("walk_l")

    def release_right(self):
        self.keepRight = False
        if not self.keepLeft:
            return
        match self.status:
            case Status.WALK:
                if self.direction == Direction.RIGHT:
                    self._turn_to(Direction.LEFT, False)
            case Status.FALLING:
                self._turn_to(Direction.LEFT, True)
            case Status.IDLE:
                self.direction = Direction.LEFT
                self.sprite.animation.play("walk_l")

    def start_falling(self):
        self.change_status(Status.FALLING)
        if self.direction == Direction.RIGHT:
            self.sprite.animation.play("fall_r")
        else:
            self.sprite.animation.play("fall_l")

    def landing(self):
        match (self.keepLeft, self.keepRight):
            case (True, False):
                self.change_status(Status.WALK)
                self.sprite.animation.play("walk_l")
            case (False, True):
                self.change_status(Status.WALK)
                self.sprite.animation.play("walk_r")
            case (True, True):
                self.change_status(Status.WALK)
                if self.direction == Direction.RIGHT:
                    self.sprite.animation.play("walk_r")
                else:
                    self.sprite.animation.play("walk_l")
            case _:
                self.stand_idle()

    def stand_idle(self):
        self.change_status(Status.IDLE)
        if self.direction == Direction.RIGHT:
            self.sprite.animation.play("idle_r")
        else:
            self.sprite.animation.play("idle_l")

    def move_to(self, x: float, y: float):
        self.position.set(x, y)
        self._syn_position()

    def move(self, x: float, y: float):
        self.position.move(x, y)
        self._syn_position()

    def process(self, delta: int):
        match (self.keepLeft, self.keepRight):
            case (True, False):
                self.speedH = max(- Duck.SPEED_H_LIMIT, self.speedH - Duck.ACCELERATION * delta)
            case (False, True):
                self.speedH = min(Duck.SPEED_H_LIMIT, self.speedH + Duck.ACCELERATION * delta)
            case _:
                self.speedH = approach(self.speedH, 0, Duck.RESISTANCE * delta)

        if self.status == Status.FALLING:
            self.speedV += Duck.GRAVITY * delta
            if self.speedV > Duck.GRAVITY_LIMIT:
                self.speedV = Duck.GRAVITY_LIMIT

        vTrend = self.speedV + Duck.GRAVITY * delta

        self.moveTrend = Vec2f(self.speedH * delta, vTrend * delta)

    def applyTrend(self, move: Vec2f, hCollided: bool, vCollided: bool, onLand: bool):
        if hCollided:
            self.speedH = 0
        if vCollided:
            self.speedV = 0

        self.move(move.x, move.y)

        if not onLand and self.status != Status.FALLING:
            self.start_falling()

        if vCollided and self.status == Status.FALLING:
            self.landing()

        if self.speedH == 0 and self.status == Status.WALK:
            self.stand_idle()
