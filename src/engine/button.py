import pygame
from .sufaceItem import SurfaceItem
from .signal import Signal


# Button module
# Default signal: pushed
class Button(SurfaceItem):

    idleImg: pygame.Surface
    pushImg: pygame.Surface

    activeOnRelease: bool = False
    '''Button emit signal when pushed or released'''
    clicked: bool = False

    def __init__(self, name: str, surface: pygame.Surface):
        super().__init__()
        self.set_idle_img(surface)
        self.clicked = False
        self.name = name
        self.signals.sign(Signal("pushed", name))

    def set_idle_img(self, surface: pygame.Surface, sameToPush: bool = True):
        self.idleImg = surface
        self.size = self.idleImg.get_rect()
        if sameToPush:
            self.pushImg = self.idleImg
        self._update_surface(False)

    def set_push_img(self, surface: pygame.Surface):
        self.pushImg = surface

    def _update_surface(self, pushed: bool):
        if pushed:
            self.surface = self.pushImg
        else:
            self.surface = self.idleImg

    def update(self, _delta: int):
        if (pygame.mouse.get_pressed()[0] == 1 and not self.clicked):
            mousePos = pygame.mouse.get_pos()
            if self.rect().collidepoint(mousePos):
                self.clicked = True
                self._update_surface(True)
                if not self.activeOnRelease:
                    self.signals.active("pushed")

        if (self.clicked and pygame.mouse.get_pressed()[0] == 0):
            self.clicked = False
            self._update_surface(False)
            if self.activeOnRelease:
                self.signals.active("pushed")
