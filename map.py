import pygame
from Obstacles.tile import Tile
from Obstacles.wall import Wall
from Obstacles.crate import Crate
from bomb import Bomb
from Utilities.settings import *
import random
from Utilities.asset_loader import AssetLoader
from Utilities.observer import Observer

class Map(Observer):
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__columns = 25
        self.__rows = 13
        self.__origin_background = pygame.transform.scale(pygame.image.load('Assets/Backgrounds/background.png').convert_alpha(), (self.__width, self.__height))
        self.__current_background = self.__origin_background
        
        self.origin_map = []
        self.__create_map()
        self.current_map = self.origin_map.copy()
        
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
            self.origin_map.append(current_row)
            current_row = []
            
        for i in range(self.__columns):
            for j in range(self.__rows):
                if (i == 0 and j == 0) or (i == self.__columns - 1 and j == 0) or (i == 0 and j == self.__rows - 1) or (i == self.__columns - 1 and j == self.__rows - 1):
                    continue
                if i % 2 == 0 and j % 2 == 0:
                    self.origin_map[j][i] = Wall(self.origin_map[j][i].x, self.origin_map[j][i].y, tile_width, tile_height)
                    
        n_crates = int(len(self.origin_map[0]) * 1) * self.__rows
        
        for i in range(n_crates):
            x = random.randint(0, self.__columns - 1)
            y = random.randint(0, self.__rows - 1)
            if (0 <= x <= 1 or self.__columns - 2 <= x <= self.__columns - 1) and (0 <= y <= 1 or self.__rows - 2 <= y <= self.__rows - 1):
                continue
            elif not isinstance(self.origin_map[y][x], Wall):
                self.origin_map[y][x] = Crate(self.origin_map[y][x].x, self.origin_map[y][x].y, tile_width, tile_height)
            
        # collidables = [wall.rect for wall in self.__playground]
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 0.88 * self.__current_w, 2))
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        # collidables.append(pygame.Rect( 0.062 * self.__current_w, 0.87 * self.__current_h, 0.88 * self.__current_w, 2))
        # collidables.append(pygame.Rect( 0.941 * self.__current_w, 0.11 * self.__current_h, 2, 0.76 * self.__current_h))
        
    def set_starting_postion(self, x: int, y: int) -> tuple:
        return (self.origin_map[y][x].x, self.origin_map[y][x].y)
        
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
        
        for row in self.current_map:
            for tile in row:
                if isinstance(tile, Wall) or isinstance(tile, Crate):
                    game_display.blit(tile.image, (tile.rect.x, tile.rect.y))
                    
    def __check_left(self, x: int, y: int, radius: int):
        for k in range(1, radius + 1):
            if 0 <= y - k < len(self.current_map[x]):
                if isinstance(self.current_map[x][y - k], Crate):
                    self.current_map[x][y - k] = Tile(self.current_map[x][y - k].rect.x, self.current_map[x][y - k].rect.y, self.current_map[x][y - k].rect.width)
                    break
                elif isinstance(self.current_map[x][y - k], Wall):
                    break
    
    def __check_right(self, x: int, y: int, radius: int):
        for k in range(1, radius + 1):
            if 0 <= y + k < len(self.current_map[x]):
                if isinstance(self.current_map[x][y + k], Crate):
                    self.current_map[x][y + k] = Tile(self.current_map[x][y + k].rect.x, self.current_map[x][y + k].rect.y, self.current_map[x][y + k].rect.width)
                    break
                elif isinstance(self.current_map[x][y + k], Wall):
                    break
    
    def __check_up(self, x: int, y: int, radius: int):
        for k in range(1, radius + 1):
            if 0 <= x - k < len(self.current_map):
                if isinstance(self.current_map[x - k][y], Crate):
                    self.current_map[x - k][y] = Tile(self.current_map[x - k][y].rect.x, self.current_map[x - k][y].rect.y, self.current_map[x - k][y].rect.width)
                    break
                elif isinstance(self.current_map[x - k][y], Wall):
                    break
    
    def __check_down(self, x: int, y: int, radius: int):
        for k in range(1, radius + 1):
            if 0 <= x + k < len(self.current_map):
                if isinstance(self.current_map[x + k][y], Crate):
                    self.current_map[x + k][y] = Tile(self.current_map[x + k][y].rect.x, self.current_map[x + k][y].rect.y, self.current_map[x + k][y].rect.width)
                    break
                elif isinstance(self.current_map[x + k][y], Wall):
                    break
            
    def update(self, object) -> None:
        if isinstance(object, Bomb):
            for row in self.current_map:
                for tile in row:
                    if isinstance(tile, Bomb):
                        x = self.current_map.index(row)
                        y = row.index(tile)
                        self.__check_left(x, y, tile.explosion_radius)
                        self.__check_right(x, y, tile.explosion_radius)
                        self.__check_up(x, y, tile.explosion_radius)
                        self.__check_down(x, y, tile.explosion_radius)
                        row[row.index(tile)] = Tile(tile.rect.x, tile.rect.y, tile.rect.width)