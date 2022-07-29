#! /usr/bin/env python3
import os
import sys
import pygame
import engine
from gamescene import gameScene

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def main():

    WINDOW_SIZE = (450, 600)
    WINDOW_FLAG = pygame.RESIZABLE | pygame.SCALED
    WINDOW_CAPTION = "Space Duck Drop!"
    engine.main.init(WINDOW_SIZE, WINDOW_FLAG, WINDOW_CAPTION)

    pygame_icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(pygame_icon)

    gameScene.init()
    engine.main.load_scene(gameScene)

    engine.main.run()


if __name__ == "__main__":
    main()
