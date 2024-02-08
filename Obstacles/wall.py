import pygame
from Utilities.settings import *

class Wall():
    def __init__(self, x: int, y: int, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('Assets/Wall/wall.png'), (width, height))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        
    def update(self, game_display: pygame.display):
        game_display.blit(self.image, (self.rect.x, self.rect.y))