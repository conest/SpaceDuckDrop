from engine.font import Font
from engine.sprite import Sprite
from engine.resource import resource
from engine.lib.vect import Vec2f


class Gamestart:
    NAME: str = "Gamestart"
    ZOOM: int = 2

    sprite: Sprite
    text: Font
    visible: True

    def __init__(self):
        name = Gamestart.NAME
        resource.add_surface(name, "assets/title.png")
        resource.scale_surface(name, Gamestart.ZOOM)

        self.name = name

        self.sprite = Sprite(resource.surface(name))
        self.sprite.name = name
        self.sprite.zIndex = 1

        resource.add_font("Retro_Gaming", "assets/Retro_Gaming.ttf", 11)
        font = Font(resource.font("Retro_Gaming"))
        font.name = "font_Gamestart"
        font.set_string("Press any key to start", (200, 200, 200))
        font.zIndex = 2
        self.text = font

    def move_to(self, x: float, y: float):
        self.sprite.position = Vec2f(x, y)
        self.text.position = Vec2f(x, y) + Vec2f(60, 200)

    def surfaces(self):
        return [self.sprite, self.text]

    def set_text(self, text: str):
        self.text.set_string(text, (200, 200, 200))

    def set_visible(self, v: bool):
        self.visible = v
        self.sprite.visible = v
        self.text.visible = v


class Gameover:
    NAME: str = "Gameover"
    ZOOM: int = 2

    sprite: Sprite
    text: Font
    visible: True

    def __init__(self):
        resource.add_surface("gameover", "assets/gameover.png")
        resource.scale_surface("gameover", Gameover.ZOOM)

        self.name = Gameover.NAME

        self.sprite = Sprite(resource.surface("gameover"))
        self.sprite.name = Gameover.NAME
        self.sprite.zIndex = 1

        resource.add_font("Retro_Gaming", "assets/Retro_Gaming.ttf", 11)
        font = Font(resource.font("Retro_Gaming"))
        font.name = "font_Gameover"
        font.set_string("The duck survived: seconds", (200, 200, 200))
        font.zIndex = 2
        self.text = font

    def move_to(self, x: float, y: float):
        self.sprite.position = Vec2f(x, y)
        self.text.position = Vec2f(x, y) + Vec2f(45, 120)

    def surfaces(self):
        return [self.sprite, self.text]

    def set_text(self, text: str):
        self.text.set_string(text, (200, 200, 200))

    def set_visible(self, v: bool):
        self.visible = v
        self.sprite.visible = v
        self.text.visible = v
