import pygame
from Utilities.settings import *
from Utilities.asset_loader import AssetLoader

class Crate():
    def __init__(self, x: int, y: int, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(AssetLoader().crate_img, (width, height))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def update(self, game_display):
        game_display.blit(self.image, (self.rect.x, self.rect.y))