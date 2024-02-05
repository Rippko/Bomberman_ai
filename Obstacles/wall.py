import pygame

class Wall():
    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y
        self.__image = pygame.transform.scale(pygame.image.load('Assets/Wall/wall.png'), (60, 60))
        self.rect = self.__image.get_rect(topleft = (self.__x, self.__y))
        
    def update(self, game_display: pygame.display):
        game_display.blit(self.__image, (self.__x, self.__y))