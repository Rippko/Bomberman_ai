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
        self.__players = []
        
        self.origin_map = []
        self.player_map = []
        self.__create_map()
        self.current_map = self.origin_map.copy()
        
        self.tile_width = self.origin_map[0][0].rect.width
        self.__current_w = self.__width
        self.__current_h = self.__height
        
    def get_players(self) -> list:
        return self.__players
        
    def calculate_game_plan_size(self) -> tuple:
        if not self.origin_map or not self.origin_map[0]:
            return

        rows, columns = len(self.origin_map), len(self.origin_map[0])

        min_x, min_y = self.origin_map[0][0].x, self.origin_map[0][0].y
        max_x, max_y = self.origin_map[0][0].x + self.origin_map[0][0].tile_size, self.origin_map[0][0].y + self.origin_map[0][0].tile_size

        for row in range(rows):
            for col in range(columns):
                tile = self.origin_map[row][col]
                min_x = min(min_x, tile.x)
                min_y = min(min_y, tile.y)
                max_x = max(max_x, tile.x + tile.tile_size)
                max_y = max(max_y, tile.y + tile.tile_size)

        return (int(min_x), int(max_x), int(min_y), int(max_y))
        
    
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
            self.player_map.append(current_row)
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
        
    def set_starting_postion(self, x: int, y: int) -> tuple:
        return (self.origin_map[y][x].x, self.origin_map[y][x].y)
    
    def add_player(self, player) -> None:
        self.__players.append(player)
        
    def resize_map(self, width: int, height: int) -> None:
        self.__current_background = pygame.transform.scale(self.__origin_background, (width, height))
        
        width_ratio = width / self.__current_w
        height_ratio = height / self.__current_h
        
        for row in self.current_map:
            for tile in row:
                tile.rect.x *= width_ratio
                tile.rect.y *= height_ratio
                tile.rect.width *= width_ratio
                tile.rect.height *= height_ratio
                
        for row in self.current_map:
            for obstacle in row:
                obstacle.rect.x *= width_ratio
                obstacle.rect.y *= height_ratio
                obstacle.rect.width *= width_ratio
                obstacle.rect.height *= height_ratio
                if type(obstacle) == Crate:
                    obstacle.image = pygame.transform.scale(AssetLoader().crate_img, (obstacle.rect.width, obstacle.rect.height))
                elif type(obstacle) == Wall:
                    obstacle.image = pygame.transform.scale(AssetLoader().wall_img, (obstacle.rect.width, obstacle.rect.height))

        self.__current_w = width
        self.__current_h = height
    
    def render_map(self, game_display: pygame.display) -> None:
        game_display.blit(self.__current_background, (0, 0))
        
        for row in self.current_map:
            for tile in row:
                if isinstance(tile, Wall) or isinstance(tile, Crate):
                    game_display.blit(tile.image, (tile.rect.x, tile.rect.y))
                    
        # for row in self.current_map:
        #     for tile in row:
        #         pygame.draw.rect(game_display, BLUE, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height), 2)
                    
    def __check_left(self, x: int, y: int, radius: int, crate_positions: list):
        for k in range(1, radius + 1):
            if 0 <= y - k < len(self.current_map[x]):
                tile = self.current_map[x][y - k]
                if isinstance(tile, Wall):
                    break
                elif isinstance(tile, Crate) or isinstance(tile, Tile):
                    crate_positions.append((tile, x, y - k))
                    if isinstance(tile, Crate):
                        break
    
    def __check_right(self, x: int, y: int, radius: int, crate_positions: list):
        for k in range(1, radius + 1):
            if 0 <= y + k < len(self.current_map[x]):
                tile = self.current_map[x][y + k]
                if isinstance(tile, Wall):
                    break
                elif isinstance(tile, Crate) or isinstance(tile, Tile):
                    crate_positions.append((tile, x, y + k))
                    if isinstance(tile, Crate):
                        break
    
    def __check_up(self, x: int, y: int, radius: int, crate_positions: list):
        for k in range(1, radius + 1):
            if 0 <= x - k < len(self.current_map):
                tile = self.current_map[x - k][y]
                if isinstance(tile, Wall):
                    break
                elif isinstance(tile, Crate) or isinstance(tile, Tile):
                    crate_positions.append((tile, x - k, y))
                    if isinstance(tile, Crate):
                        break
    
    def __check_down(self, x: int, y: int, radius: int, crate_positions: list):
        for k in range(1, radius + 1):
            if 0 <= x + k < len(self.current_map):
                tile = self.current_map[x + k][y]
                if isinstance(tile, Wall):
                    break
                elif isinstance(tile, Crate) or isinstance(tile, Tile):
                    crate_positions.append((tile, x + k, y))
                    if isinstance(tile, Crate):
                        break
       
    def __destroy_crates(self, tiles: dict) -> None:
        for key in tiles:
            for tile, x, y in tiles[key]:
                if isinstance(tile, Crate):
                    self.current_map[x][y] = Tile(tile.rect.x, tile.rect.y, tile.rect.width)
                    
    def __check_player_position(self, explosion_tiles: dict) -> None:
        for player in self.__players:
            for key in explosion_tiles:
                for tile, x, y in explosion_tiles[key]:
                    if player.check_position(tile):
                        player.set_dead()

   
    def update(self, object) -> None:
        if isinstance(object, Bomb):
            explosion_tiles = {'up': [], 'down': [], 'left': [], 'right': [], 'center': []}
            for row in self.current_map:
                for tile in row:
                    if tile == object:
                        x = self.current_map.index(row)
                        y = row.index(tile)
                        explosion_tiles['center'].append((tile, x, y))
                        self.__check_left(x, y, tile.explosion_radius, explosion_tiles['left'])
                        self.__check_right(x, y, tile.explosion_radius, explosion_tiles['right'])
                        self.__check_up(x, y, tile.explosion_radius, explosion_tiles['up'])
                        self.__check_down(x, y, tile.explosion_radius, explosion_tiles['down'])
                        object.set_explosion(explosion_tiles)
                        self.__check_player_position(explosion_tiles)
                        self.__destroy_crates(explosion_tiles)
                        row[row.index(tile)] = Tile(tile.rect.x, tile.rect.y, self.tile_width)