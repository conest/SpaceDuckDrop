'''A simple Physical lib'''
from pygame import Rect
from .vect import Vec2f


def approach(s: Rect, des: Rect, m: Vec2f, t: Rect) -> tuple[Vec2f, bool, bool]:
    '''Test a moving source Rect s, with movement move, will collide target t.\
        Return a Rect that amount of movement, and bools for indicate if horizontal\
        or vertical collided.\
        (With an excessive movement, source may go through the target without\
        collide detected)'''

    # s: Source hitbox
    # des: Destination hitbox
    # m: movement (in float, for smooth movement)
    # t: Target hitbox

    if not des.colliderect(t):
        return (m, False, False)

    # Calculate the closest distance
    xdis: float = 0
    ydis: float = 0

    if m.x >= 0:
        xdis = t.x - (s.x + s.w)
    else:
        xdis = s.x - (t.x + t.w)

    if m.y >= 0:
        ydis = t.y - (s.y + s.h) + 1
    else:
        ydis = s.y - (t.y + t.h)

    ratio: float
    hCollided: bool = False
    vCollided: bool = False

    if xdis > ydis:
        hCollided = True
        if xdis <= 0:
            m.x = 0
        else:
            m.x = xdis
    else:
        vCollided = True
        if ydis <= 0:
            m.y = 0
        else:
            m.y = ydis

    return (m, hCollided, vCollided)
