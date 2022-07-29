import pygame

keys = {
    "RIGHT": (pygame.K_RIGHT, pygame.K_d),
    "LEFT": (pygame.K_LEFT, pygame.K_a),
}


def readkey(event: pygame.event.Event) -> str:
    for keyname, keytuple in keys.items():
        for key in keytuple:
            if event.key == key:
                return keyname
    return None
