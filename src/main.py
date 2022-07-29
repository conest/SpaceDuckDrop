#! /usr/bin/env python3
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import engine
from gamescene import gameScene


def main():
    WINDOW_SIZE = (450, 600)
    WINDOW_FLAG = pygame.RESIZABLE | pygame.SCALED
    WINDOW_CAPTION = "Space Duck Drop!"
    engine.main.init(WINDOW_SIZE, WINDOW_FLAG, WINDOW_CAPTION)

    gameScene.init()
    engine.main.load_scene(gameScene)

    engine.main.run()


if __name__ == "__main__":
    main()
