import pygame
from Utilities.settings import *

class Tile ():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.isWall = False
        self.rect = pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)
        