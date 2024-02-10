import pygame
from Utilities.settings import *

class Tile ():
    def __init__(self, x, y, tile_size) -> None:
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.isEmpty = True
        self.rect = pygame.Rect(self.x, self.y, self.tile_size, self.tile_size)
        