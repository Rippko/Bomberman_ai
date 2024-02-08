import pygame
from Utilities.settings import *
from Utilities.asset_loader import AssetLoader

class Wall():
    def __init__(self, x: int, y: int, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(AssetLoader().wall_img, (width, height))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        
    def update(self, game_display: pygame.display):
        game_display.blit(self.image, (self.rect.x, self.rect.y))