import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .scene import Scene

BACKGROUND_COLOR = pygame.Color(128, 128, 128)

_inited: bool = False
screen: pygame.Surface
fpsLimit: int = 60
scene: Scene = None


def isInited() -> bool:
    return _inited


def init(windowSize: tuple, flag: int, caption: str, vsync: int = 1):
    global _inited
    global screen
    pygame.init()
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode(windowSize, flag, vsync=vsync)
    _inited = True


def default_init():
    WINDOW_SIZE = (800, 450)
    WINDOW_FLAG = pygame.RESIZABLE | pygame.SCALED
    WINDOW_CAPTION = "My Awesome Game"
    init(WINDOW_SIZE, WINDOW_FLAG, WINDOW_CAPTION, vsync=1)


def set_fps(fps: int):
    global fpsLimit
    fpsLimit = fps


def load_scene(s: Scene):
    global scene
    scene = s


def run():
    assert(_inited), "Engine must be initialized first!"
    assert(scene), "A scene must be loaded!"

    global screen
    fps = pygame.time.Clock()
    running = True

    while running:
        delta: int = fps.tick(fpsLimit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.event_handle(event, delta)

        scene.update(delta)
        scene.process(delta)
        scene.signal_handle()

        screen.fill(BACKGROUND_COLOR)
        scene.draw(screen)
        pygame.display.update()
