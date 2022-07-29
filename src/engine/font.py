import pygame
from .sufaceItem import SurfaceItem


class Font(SurfaceItem):
    font: pygame.font.Font

    def __init__(self, font: pygame.font.Font):
        super().__init__()
        self.name = "Font"
        self.load_font(font)

    def load_font(self, font: pygame.font.Font):
        self.font = font

    def set_string(self, string: str, color: tuple = (0, 0, 0)):
        ns = self.font.render(string, False, color)
        self._update(ns)

    def _update(self, ns: pygame.Surface):
        self.surface = pygame.Surface((ns.get_width(), ns.get_height()), pygame.SRCALPHA).convert_alpha()
        self.surface.blit(ns, (0, 0))
