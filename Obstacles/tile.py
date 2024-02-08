import pygame
from Utilities.settings import *

class Tile ():
    def __init__(self, x, y, tile_size) -> None:
        self.x = x
        self.y = y
        self.isEmpty = False
        self.rect = pygame.Rect(self.x, self.y, tile_size, tile_size)
        