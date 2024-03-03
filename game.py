import pygame, time
from Entities.player import Player
from map import Map
from Utilities.settings import *

class Game():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.FPS = 60
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption('Bomberman')
        self.__fullscreen = False
        self.__monitor_resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.__clock = pygame.time.Clock()
        
        self.__map = Map(self.__width, self.__height)
        self.__player = Player(self.__map.set_starting_postion(0, 0), 'player_character_purple', (8, 7, 4), 32, 32, 2, self.__map, self.__screen)
        
        self.__map.add_player(self.__player)

        self.font = pygame.font.Font('Assets/Fonts/VCR_OSD_MONO_1.001.ttf', (35 * self.__height // self.__height))
        
        self.__last_time = time.time()
        
    def __handle_windowed(self, width: int, height: int) -> None:
        self.__screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.__map.resize_map(width, height)

    def __handle_fullscreen(self):
        self.__screen = pygame.display.set_mode(self.__monitor_resolution, pygame.FULLSCREEN)
        self.__map.resize_map(self.__monitor_resolution[0], self.__monitor_resolution[1])

    def __handle_events(self) -> None:
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
                            
    def __draw_text(self, text: str, x: int, y: int) -> None:
        text_surface = self.font.render(text, True, BLACK)
        self.__screen.blit(text_surface, (x, y))
        
    def run(self) -> None:
        while True:
            current_time = time.time()
            delta_time = current_time - self.__last_time
            self.__last_time = current_time
            
            self.__map.render_map(self.__screen)
            
            self.__draw_text('PLAYER 1', (10 * self.__width // self.__width), (5 * self.__height // self.__height))
            
            self.__handle_events()
            
            pressed_keys = pygame.key.get_pressed()
            
            self.__player.handle_keypress(pressed_keys)
            
            self.__player.update(pressed_keys, delta_time)
            
            self.__clock.tick(self.FPS)
            pygame.display.flip()