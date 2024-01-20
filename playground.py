import pygame
from Entities.player import Player
from Utilities.colors import Colors

class Playground():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__player = Player(100, 100, 'player_character', 4, 32, 34, 2)
        
    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Bomberman")
        
        collidables = []
        collidables.append(pygame.Rect((180, 180, 70, 70)))
        collidables.append(pygame.Rect((250, 250, 70, 70)))
        collidables.append(pygame.Rect((300, 450, 70, 70)))
        
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            
            pressed_keys = pygame.key.get_pressed()
            
            self.__player.handle_keypress(pressed_keys)
                        
            self.__screen.fill(Colors.GREY)
            
            
            for tile in collidables:
                pygame.draw.rect(self.__screen, Colors.BLACK, tile)

            self.__player.update(self.__screen, pressed_keys, collidables)
                        
            pygame.display.update()
            clock.tick(60)
            
                    