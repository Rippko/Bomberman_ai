import pygame
from Entities.player import Player
from Utilities.settings import *
from Obstacles.tile import Tile
from Obstacles.wall import Wall
from Obstacles.crate import Crate
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
        
        self.__player = Player(self.__origin_grid[0][0].x, self.__origin_grid[0][1].y, 'player_character', 4, 32, 32, 2)
        self.__fullscreen = False
        self.__monitor_resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        
    def __create_playground(self) -> None:
        cols = 25
        rows = 13

        x1, y1 = 0.062 * self.__current_w, 0.11 * self.__current_h
        x2, y2 = 0.941 * self.__current_w, 0.11 * self.__current_h

        width = x2 - x1
        
        tile_width = width / cols
        
        x3, y3 = 0.941 * self.__current_w, 0.11 * self.__current_h
        x4, y4 = 0.941 * self.__current_w, 0.87 * self.__current_h

        height = y4 - y3
        
        tile_height = height / rows

        current_row = []
        for i in range(rows):
            for j in range(cols):
                current_row.append(Tile(x1 + j * tile_width, y1 + i * tile_height, tile_width))
            self.__origin_grid.append(current_row)
            current_row = []


        for i in range(cols):
            for j in range(rows):
                if (i == 0 and j == 0) or (i == cols - 1 and j == 0) or (i == 0 and j == rows - 1) or (i == cols - 1 and j == rows - 1):
                    continue
                if i % 2 == 0 and j % 2 == 0:
                    self.__playground.append(Wall(self.__origin_grid[j][i].x, self.__origin_grid[j][i].y, tile_width, tile_height))
                    self.__origin_grid[j][i].isWall = True

        n_crates = 120
        for i in range(n_crates):
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            if self.__origin_grid[y][x].isWall or (x == 0 and y == 0) or (x == cols - 1 and y == rows - 1) or (x == 0 and y == rows - 1) or (x == cols - 1 and y == 0) or (x == 1 and y == 0) or (x == 0 and y == 1) or (x == cols - 2 and y == rows - 1) or (x == cols - 1 and y == rows - 2) or (x == 1 and y == rows - 1) or (x == 0 and y == rows - 2) or (x == cols - 2 and y == 0) or (x == cols - 1 and y == 1) or (x == 1 and y == 1) or (x == 1 and y == rows - 2) or (x == cols - 2 and y == 1):
                continue
            self.__playground.append(Crate(self.__origin_grid[y][x].x, self.__origin_grid[y][x].y, tile_width, tile_height))
            self.__origin_grid[y][x].isWall = True
        
    
    def __resize_grid(self, width: int, height: int) -> None:
        width_ratio = width / self.__current_w
        height_ratio = height / self.__current_h
        
        for row in self.__grid:
            for tile in row:
                tile.rect.x *= width_ratio
                tile.rect.y *= height_ratio
                tile.rect.width *= width_ratio
                tile.rect.height *= height_ratio

        for wall in self.__playground:
            wall.rect.x *= width_ratio
            wall.rect.y *= height_ratio
            wall.rect.width *= width_ratio
            wall.rect.height *= height_ratio
            wall.image = pygame.transform.scale(wall.image, (wall.rect.width, wall.rect.height))

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
        collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 0.88 * self.__current_w, 2))
        collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.87 * self.__current_h, 0.88 * self.__current_w, 2))
        collidables.append(pygame.Rect( 0.941 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        
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

            # for row in self.__origin_grid:
            #     for tile in row:
            #         pygame.draw.rect(self.__screen, BLUE, tile.rect, 2, 2)

            for coll in collidables:
                pygame.draw.rect(self.__screen, RED, coll, 2)
            
            for wall in self.__playground:
                wall.update(self.__screen)
                # pygame.draw.rect(self.__screen, RED, wall, 2, 2)
            

            self.__player.update(self.__screen, pressed_keys, collidables)
                        
            pygame.display.update()
            clock.tick(60)