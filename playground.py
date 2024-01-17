import pygame
import sys
from Entities.player import Player
from Utilities.colors import Color

class Playground():
    def __init__(self, width, height) -> None:
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__player = Player()
        
    def run(self):
        clock = pygame.time.Clock()
        
        pygame.init()
        pygame.display.set_caption("Bomberman")
        
        self.__screen.fill(Color.GREY)
        
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
            
                    