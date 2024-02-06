import pygame
from Entities.player import Player
from Utilities.settings import *
from Obstacles.tile import Tile
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
        
        self.__origin_grid = []
        self.__playground = []
        self.__create_playground()
        print(len(self.__origin_grid))
        
        self.__grid = self.__origin_grid.copy()
        
        self.__player = Player(self.__origin_grid[0].x, self.__origin_grid[0].y, 'player_character', 4, 32, 32, 2)
        self.__fullscreen = False
        self.__monitor_resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        
    def __create_playground(self) -> None:
        x1, y1 = 0.062 * self.__current_w, 0.11 * self.__current_h
        x2, y2 = 0.941 * self.__current_w, 0.11 * self.__current_h

        width = x2 - x1
        
        tile_width = width / 26
        
        x3, y3 = 0.941 * self.__current_w, 0.11 * self.__current_h
        x4, y4 = 0.941 * self.__current_w, 0.87 * self.__current_h

        height = y4 - y3
        
        tile_height = height / 13

        for i in range(26):
            x = x1 + i * tile_width
            for j in range(13):
                y = y1 + j * tile_height
                self.__origin_grid.append(Tile(x, y))
                
        n_walls = len(self.__origin_grid) // 3
        for i in range(n_walls):
            index = random.randint(0, len(self.__origin_grid) - 1)
            if not self.__origin_grid[index].isWall:
                self.__playground.append(Wall(self.__origin_grid[index].x, self.__origin_grid[index].y, tile_width, tile_height))
                self.__origin_grid[index].isWall = True
            else:
                n_walls += 1
        
    
    def __resize_grid(self, width: int, height: int) -> None:
        width_ratio = width / self.__current_w
        height_ratio = height / self.__current_h
        
        for i in range(len(self.__grid)):
            self.__grid[i].rect.left = int(self.__origin_grid[i].rect.left * width_ratio)
            self.__grid[i].rect.top = int(self.__origin_grid[i].rect.top * height_ratio)
            
            self.__grid[i].rect.width = int(self.__origin_grid[i].rect.width * width_ratio)
            self.__grid[i].rect.height = int(self.__origin_grid[i].rect.height * height_ratio)

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
        collidables = [wall.rect for wall in self.__playground]
        
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
            
            # for tile in self.__grid:
            #     pygame.draw.rect(self.__screen, BLUE, tile.rect, 2, 2)
            
            for wall in self.__playground:
                wall.update(self.__screen)
                # pygame.draw.rect(self.__screen, RED, wall, 2, 2)
            

            self.__player.update(self.__screen, pressed_keys, collidables)
                        
            pygame.display.flip()
            clock.tick(60)