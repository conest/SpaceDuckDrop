import pygame
from .sufaceItem import SurfaceItem


class TextContainer(SurfaceItem):
    font: pygame.font.Font
    fontColor: pygame.Color

    text: list
    textLimit: int
    lineLimit: int
    lineSpacing: int

    backgroundColor: pygame.Color

    def __init__(self, size: pygame.Rect, font: pygame.font.Font):
        super().__init__()
        self.name = "TextContainer"
        self.size = size

        self.load_font(font)
        self.text = []
        self.textLimit = 5
        self.lineSpacing = 16

        self.backgroundColor = pygame.Color(200, 200, 200)
        self.fontColor = pygame.Color(0, 0, 0)

    def load_font(self, font: pygame.font.Font):
        self.font = font

    def set_font_color(self, color: tuple = (0, 0, 0)):
        self.fontColor = color

    def _check_text_length(self, string: str) -> list:
        '''Work only with Roman alphabet!'''

        length = self.font.size(string)[0]
        stringList: list = []
        if (length <= self.size.w):
            stringList.append(string)
            return stringList

        while True:
            sr = self._split_string(string)
            stringList.append(sr[0])
            if sr[1] is None:
                break
            length = self.font.size(sr[1])[0]
            if (length > self.size.w):
                string = sr[1]
            else:
                stringList.append(sr[1])
                break

        return stringList

    def _split_string(self, string: str) -> tuple:
        splitedString: list = string.split()
        if len(splitedString) == 1:
            return (string, None)

        maxWordIndex: int = 0
        testString: str = splitedString[0]
        while True:
            length = self.font.size(testString)[0]
            if length > self.size.w:
                break
            if maxWordIndex >= len(splitedString) - 1:
                break
            maxWordIndex += 1
            testString += f" {splitedString[maxWordIndex]}"

        firstString: str = splitedString[0]
        for i in range(1, maxWordIndex):
            firstString += f" {splitedString[i]}"

        secondString: str = splitedString[maxWordIndex]
        for i in range(maxWordIndex + 1, len(splitedString)):
            secondString += f" {splitedString[i]}"

        return (firstString, secondString)

    def add_text(self, string: str, useDefaultColor: bool = True, fontColor: tuple = (0, 0, 0)):
        stringList: list = self._check_text_length(string)
        if (len(stringList) > 1):
            for i in range(0, len(stringList)):
                self.add_text(stringList[i])
            return

        textnum: int = len(self.text)
        if (textnum >= self.textLimit):
            self.text.pop(0)
            textnum = len(self.text)
        self.text.append(string)

        textSurface: pygame.Surface
        if useDefaultColor:
            textSurface = self.font.render(string, False, self.fontColor)
        else:
            textSurface = self.font.render(string, False, fontColor)

        newSurface = pygame.Surface((self.size.w, self.size.h), pygame.SRCALPHA)
        newSurface.fill(self.backgroundColor)

        if textnum > 0:
            oldY = self.size.h - (textnum + 1) * self.lineSpacing
            drawRect = pygame.Rect(0, oldY + self.lineSpacing, self.size.w, textnum * self.lineSpacing)
            newSurface.blit(self.surface, (0, oldY), drawRect)

        newY: float = self.size.h - self.lineSpacing
        newSurface.blit(textSurface, (0, newY))
        self.surface = newSurface
