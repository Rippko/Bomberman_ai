import pygame
from Obstacles.tile import Tile
from Obstacles.wall import Wall
from Obstacles.crate import Crate
from Utilities.settings import *
import random
from Utilities.asset_loader import AssetLoader

class Map():
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__columns = 25
        self.__rows = 13
        self.__origin_background = pygame.transform.scale(pygame.image.load('Assets/Backgrounds/background.png').convert_alpha(), (self.__width, self.__height))
        self.__current_background = self.__origin_background
        self.grid = []
        self.map = []
        self.__create_map()
        self.__current_w = self.__width
        self.__current_h = self.__height
    
    def __create_map(self) -> None:
        x1, y1 = 0.062 * self.__width, 0.11 * self.__height
        x2, y2 = 0.941 * self.__width, 0.11 * self.__height
        width = x2 - x1
        tile_width = width / self.__columns
        x3, y3 = 0.941 * self.__width, 0.11 * self.__height
        x4, y4 = 0.941 * self.__width, 0.87 * self.__height
        height = y4 - y3
        tile_height = height / self.__rows
        current_row = []
        for i in range(self.__rows):
            for j in range(self.__columns):
                current_row.append(Tile(x1 + j * tile_width, y1 + i * tile_height, tile_width))
            self.grid.append(current_row)
            current_row = []
        
        for i in range(self.__columns):
            for j in range(self.__rows):
                if (i == 0 and j == 0) or (i == self.__columns - 1 and j == 0) or (i == 0 and j == self.__rows - 1) or (i == self.__columns - 1 and j == self.__rows - 1):
                    continue
                if i % 2 == 0 and j % 2 == 0:
                    self.map.append(Wall(self.grid[j][i].x, self.grid[j][i].y, tile_width, tile_height))
                    self.grid[j][i].isEmpty = False
                    
                # elif i % 2 != 0 and j % 2 != 0:
                #     self.map.append(Crate(self.__grid[j][i].x, self.__grid[j][i].y, tile_width, tile_height))
                #     self.__grid[j][i].isEmpty = False

        n_crates = int(len(self.map) / 1)
        print(n_crates)
        for i in range(n_crates):
            x = random.randint(0, self.__columns - 1)
            y = random.randint(0, self.__rows - 1)
            if self.grid[y][x].isEmpty and (0 <= x <= 1 or self.__columns - 2 <= x <= self.__columns - 1) and (0 <= y <= 1 or self.__rows - 2 <= y <= self.__rows - 1):
                continue
            self.map.append(Crate(self.grid[y][x].x, self.grid[y][x].y, tile_width, tile_height))
            self.grid[y][x].isEmpty = False
            
        # collidables = [wall.rect for wall in self.__playground]
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 0.88 * self.__current_w, 2))
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.87 * self.__current_h, 0.88 * self.__current_w, 2))
        # collidables.append(pygame.Rect( 0.941 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        
            
    def set_starting_postion(self, x: int, y: int) -> tuple:
        return (self.grid[y][x].x, self.grid[y][x].y)
        
    def resize_map(self, width: int, height: int) -> None:
        self.__current_background = pygame.transform.scale(self.__origin_background, (width, height))
        
        width_ratio = width / self.__current_w
        height_ratio = height / self.__current_h
        
        for row in self.grid:
            for tile in row:
                tile.rect.x *= width_ratio
                tile.rect.y *= height_ratio
                tile.rect.width *= width_ratio
                tile.rect.height *= height_ratio

        for wall in self.map:
            wall.rect.x *= width_ratio
            wall.rect.y *= height_ratio
            wall.rect.width *= width_ratio
            wall.rect.height *= height_ratio
            if type(wall) == Crate:
                wall.image = pygame.transform.scale(AssetLoader().crate_img, (wall.rect.width, wall.rect.height))
            elif type(wall) == Wall:
                wall.image = pygame.transform.scale(AssetLoader().wall_img, (wall.rect.width, wall.rect.height))

        self.__current_w = width
        self.__current_h = height
    
    def render_map(self, game_display: pygame.display) -> None:
        game_display.blit(self.__current_background, (0, 0))
        
        for row in self.grid:
            for tile in row:
                pygame.draw.rect(game_display, BLUE, tile.rect, 2, 2)
                
        for obstacle in self.map:
            obstacle.update(game_display)
            
    def update(self, game_display: pygame.display) -> None:
        self.render_map(game_display)