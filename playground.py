import pygame
from Entities.player import Player
from Utilities.colors import Colors
from Obstacles.wall import Wall
from bomb import Bomb
import random

class Playground():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.RESIZABLE)
        self.__origin_background = pygame.transform.scale(pygame.image.load('Assets/Backgrounds/background.png'), (self.__width, self.__height))
        self.__current_background = self.__origin_background
        self.__current_w = self.__screen.get_width()
        self.__current_h = self.__screen.get_height()
        self.__player = Player(110, 110, 'player_character', 4, 32, 32, 2)
        self.__playground = self.__create_playground()
        self.__fullscreen = False
        self.__monitor_resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        
        
        
        
        self.__grid = []
        # self.__grid.append(pygame.Rect(0.06 * self.__current_w, 0.1 * self.__current_h, 0.88 * self.__current_w, 1))
        # self.__grid.append(pygame.Rect(0.06 * self.__current_w, 0.1 * self.__current_h, 1, 0.77 * self.__current_h))
        # self.__grid.append(pygame.Rect(0.06 * self.__current_w, 0.89 * self.__current_h, 0.88 * self.__current_w, 1))
        # self.__grid.append(pygame.Rect(0.94 * self.__current_w, 0.1 * self.__current_h, 1, 0.77 * self.__current_h))
        
    def __create_playground(self) -> list:
        grid_width = 0.89 * self.__current_w
        grid_height = 0.80 * self.__current_h
        cell_size = 65

        playground = []

        rows = int(grid_height / cell_size)
        cols = int(grid_width / cell_size)

        for row in range(rows):
            for col in range(cols):
                x = 0.06 * self.__current_w + col * cell_size
                y = 0.1 * self.__current_h + row * cell_size
                create_wall = random.choice([True, False, False])

                if create_wall:
                    playground.append(Wall(x, y))

        return playground
        
    
    def __resize_grid(self, width: int, height: int) -> None:
        width_ratio = width / self.__current_w
        height_ratio = height / self.__current_h
        
        for i in range(len(self.__grid)):
            self.__grid[i].left = int(self.__grid[i].left * width_ratio)
            self.__grid[i].top = int(self.__grid[i].top * height_ratio)
            
            self.__grid[i].width = int(self.__grid[i].width * width_ratio)
            self.__grid[i].height = int(self.__grid[i].height * height_ratio)

        self.__current_w = width
        self.__current_h = height
        
    def __handle_windowed(self, width: int, height: int) -> None:
        self.__current_background = pygame.transform.scale(self.__origin_background, (width, height))
        self.__screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.__resize_grid(width, height)

        
    def __handle_fullscreen(self):
        self.__current_background = pygame.transform.scale(self.__origin_background, self.__monitor_resolution)
        self.__screen = pygame.display.set_mode(self.__monitor_resolution, pygame.FULLSCREEN)
        self.__resize_grid(self.__monitor_resolution[0], self.__monitor_resolution[1])
        
    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Bomberman")
        collidables = []
        # collidables = [wall.rect for wall in self.__playground]
        # collidables.extend(self.__grid)
        
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

            self.__screen.blit(self.__current_background, (0, 0))
            
            # for tile in collidables:
            #     pygame.draw.rect(self.__screen, Colors.BLACK, tile)
            
            # for wall in self.__playground:
            #     wall.update(self.__screen)
                
            for wall in self.__playground:
                pygame.draw.rect(self.__screen, Colors.RED, wall, 2, 2)
                

            for rect in self.__grid:
                pygame.draw.rect(self.__screen, Colors.RED, rect, 5)
                

            self.__player.update(self.__screen, pressed_keys, collidables)
                        
            pygame.display.flip()
            clock.tick(60) 