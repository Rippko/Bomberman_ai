import pygame
from Entities.player import Player
from Utilities.colors import Colors

class Playground():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.RESIZABLE)
        self.__origin_background = pygame.transform.scale(pygame.image.load('Assets/Backgrounds/background.png'), (self.__width, self.__height))
        self.__current_background = self.__origin_background
        self.__player = Player(100, 100, 'player_character4', 1, 25, 45, 1.9)
        self.__fullscreen = False
        self.__monitor_resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        
    def __handle_windowed(self, width: int, height: int) -> None:
        self.__current_background = pygame.transform.scale(self.__origin_background, (width, height))
        self.__screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
    def __handle_fullscreen(self):
        self.__current_background = pygame.transform.scale(self.__origin_background, self.__monitor_resolution)
        self.__screen = pygame.display.set_mode(self.__monitor_resolution, pygame.FULLSCREEN)
        
    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Bomberman")
        
        collidables = []
        collidables.append(pygame.Rect((180, 180, 90, 90)))
        collidables.append(pygame.Rect((280, 180, 80, 80)))
        #collidables.append(pygame.Rect((370, 180, 70, 70)))
        #collidables.append(pygame.Rect((250, 250, 70, 70)))
        #collidables.append(pygame.Rect((300, 450, 70, 70)))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    if not self.__fullscreen:
                        self.__handle_windowed(event.w, event.h)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_f:
                        self.__fullscreen = not self.__fullscreen
                        if self.__fullscreen:
                            self.__handle_fullscreen()
                        else:
                            self.__handle_windowed(self.__screen.get_width(), self.__screen.get_height())
            
            pressed_keys = pygame.key.get_pressed()
            
            self.__player.handle_keypress(pressed_keys)
                        
            #self.__screen.fill(Colors.GREY)
            
            wall = pygame.image.load('Assets/Wall/wall.png')
            
            
            self.__screen.blit(self.__current_background, (0, 0))
            self.__screen.blit(wall, (300, 300))
            
            for tile in collidables:
                pygame.draw.rect(self.__screen, Colors.BLACK, tile)

            self.__player.update(self.__screen, pressed_keys, collidables)
                        
            pygame.display.update()
            clock.tick(60) 