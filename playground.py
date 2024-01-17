import pygame
from Entities.player import Player
from Utilities.colors import Colors

class Playground():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__player = Player()
        
    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Bomberman")
        
        
        self.__screen.fill(Colors.GREY)
        
        self.__player.update(self.__screen)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                        
            pygame.display.update()
            clock.tick(60)
            
                    