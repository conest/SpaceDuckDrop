import random
import functools
import itertools
from enum import Enum, auto

import pygame

from engine.scene import Scene
from engine.lib import spl
from engine.lib.vect import Vec2f
from engine.resource import resource

from keys import readkey
from duck import Duck
from space_platform import Platform
from space_background import Background
from ui import Gamestart, Gameover

PLATFORM_INI_TIME = 1000
SCROLL_SPEED = 0.09
SPEED_GAIN = 0.000002


class Stage(Enum):
    START = auto()
    PLAY = auto()
    OVER = auto()


def init(self: Scene):
    self.platforms = []
    self.stage = Stage.START
    self.surviveTime = pygame.time.Clock()

    self.windowRect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())

    resource.add_surface("platform", "assets/platform.png")
    resource.scale_surface("platform", Platform.ZOOM)

    self._gen_background()

    gs = Gamestart()
    gs.move_to(75, 150)
    self.objects[Gamestart.NAME] = gs
    self.add_surfaces(gs.surfaces())

    over = Gameover()
    over.move_to(75, 200)
    self.objects[Gameover.NAME] = over
    self.add_surfaces(over.surfaces())
    over.set_visible(False)

    self.reset()


def reset(self):
    self.scrollSpeed = SCROLL_SPEED
    self.plGenTime = PLATFORM_INI_TIME
    self.plTimer = 0

    duck = Duck()
    duck.move_to(193, 436)
    self.objects[Duck.NAME] = duck
    self.add_surface(duck.sprite)
    # self.add_surface(duck.visualizedHB)

    pl = Platform(resource.surface("platform"), pygame.time.get_ticks())
    pl.generate(3)
    pl.move_to(177, 500)
    self.platforms.append(pl)
    self.add_surface(pl.image)

    self.sort_surfaces()


def change_stage(self):
    match self.stage:
        case Stage.START:
            self.objects[Gamestart.NAME].set_visible(False)
            self.stage = Stage.PLAY
            self.surviveTime.tick()
            self.objects[Duck.NAME].sprite.animation.play("awake")
            self.objects[Duck.NAME].sprite.animation.set_next("idle_r")
        case Stage.OVER:
            self.stage = Stage.START
            self.objects[Gameover.NAME].set_visible(False)
            self.objects[Gamestart.NAME].set_visible(True)

            for pf in self.platforms:
                self._delete_platform_surface(pf.name)
            self.platforms.clear()

            self.reset()


def event_handle(self: Scene, event: pygame.event.Event, delta: int):
    if self.stage != Stage.PLAY:
        if event.type == pygame.KEYDOWN:
            self.change_stage()
        return

    if event.type == pygame.KEYDOWN:
        key = readkey(event)
        if key is None:
            return
        match key:
            case "LEFT":
                self.objects[Duck.NAME].go_left()
            case "RIGHT":
                self.objects[Duck.NAME].go_right()

    if event.type == pygame.KEYUP:
        key = readkey(event)
        if key is None:
            return
        match key:
            case "LEFT":
                self.objects[Duck.NAME].release_left()
            case "RIGHT":
                self.objects[Duck.NAME].release_right()


def _gen_platform(self):
    pl = Platform(resource.surface("platform"), pygame.time.get_ticks())
    pl.generate(random.randint(1, 9))
    x = random.randint(-20, 280)
    pl.move_to(x, 601)
    self.platforms.append(pl)
    self.add_surface(pl.image)
    self.sort_surfaces()


def _gen_background(self):
    resource.add_surface("space", "assets/space.png")
    resource.scale_surface("space", Background.ZOOM)
    for x, y in itertools.product(range(4), range(5)):
        name = f'space{x}{y}'
        space = Background(name, resource.surface("space"))
        space.move_to(x * 128, y * 128)
        self.objects[name] = space
        self.add_surface(space.sprite)


def _delete_platform_surface(self, name: str):
    for i, o in enumerate(self.surfaceGroup):
        if o.name == name:
            del self.surfaceGroup[i]
            break


def _delete_platform_list(self, name: str):
    for i, o in enumerate(self.platforms):
        if o.name == name:
            del self.platforms[i]
            break


def process(self: Scene, delta: int):
    if self.stage != Stage.PLAY:
        return

    duck: Duck = self.objects[Duck.NAME]
    duck.process(delta)

    hCollided = vCollided = False
    moveTrend: Vec2f = duck.moveTrend
    des = duck.des_hitbox()
    onLand = False

    for pl in self.platforms:
        (move, hc, vc) = spl.approach(duck.hitbox, des, moveTrend, pl.hitbox)
        if hc:
            hCollided = True
        if vc:
            vCollided = True
        moveTrend = move

        if duck.feet_hitbox().colliderect(pl.hitbox):
            onLand = True

    duck.applyTrend(moveTrend, hCollided, vCollided, onLand)

    if onLand:
        self.scrollSpeed += SPEED_GAIN * delta
    self.objects[Duck.NAME].move(0, - self.scrollSpeed * delta)
    for pf in self.platforms:
        pf.move(0, - self.scrollSpeed * delta)
        if pf.position.y < - 32:
            self._delete_platform_surface(pf.name)
            self._delete_platform_list(pf.name)

    self.plTimer += delta
    if self.plTimer >= self.plGenTime:
        self.plTimer -= self.plGenTime
        self._gen_platform()

    if not duck.hitbox.colliderect(self.windowRect):
        self._game_over()


def _game_over(self):
    self.stage = Stage.OVER
    del self.objects[Duck.NAME]
    for i, o in enumerate(self.surfaceGroup):
        if o.name == Duck.NAME:
            del self.surfaceGroup[i]
            break
    gameover: Gameover = self.objects[Gameover.NAME]
    st = self.surviveTime.tick()
    gameover.set_text(f'The duck survived: {st/1000}s')
    gameover.set_visible(True)


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
gameScene.process = functools.partial(process, gameScene)
gameScene.reset = functools.partial(reset, gameScene)
gameScene.change_stage = functools.partial(change_stage, gameScene)
gameScene._delete_platform_surface = functools.partial(_delete_platform_surface, gameScene)
gameScene._delete_platform_list = functools.partial(_delete_platform_list, gameScene)
gameScene._gen_platform = functools.partial(_gen_platform, gameScene)
gameScene._gen_background = functools.partial(_gen_background, gameScene)
gameScene._game_over = functools.partial(_game_over, gameScene)
