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
        self._columns = 25
        self._rows = 13
        self.__origin_background = pygame.transform.scale(pygame.image.load('Assets/Backgrounds/background.png').convert_alpha(), (self.__width, self.__height))
        self.__current_background = self.__origin_background
        self.__players = []
        self.bombs = pygame.sprite.Group()
        self.origin_map = []
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
        
    def get_map_state(self, player_position):
        local_map_vector = []
        if player_position is not None:
            x, y = player_position
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if 0 <= x + dx < len(self.current_map[0]) and 0 <= y + dy < len(self.current_map):
                        tile = self.current_map[y + dy][x + dx]
                        if type(tile) == Tile:
                            local_map_vector.append(0)
                        elif type(tile) == Wall:
                            local_map_vector.append(1)
                        elif type(tile) == Crate:
                            local_map_vector.append(2)
                        elif type(tile) == Bomb:
                            local_map_vector.append(3)
                    else:
                        local_map_vector.append(1)
        
            local_map_vector[4] = 4
            
            return local_map_vector
        return None
    
    def step(self, action, player):
        if player is None:
            return
        else:
            player.action_map[action]()
            new_state = self.get_map_state(player.get_position())
            reward = self.__calculate_reward(action, new_state, player)
            done  = self.__check_if_game_over(player)
            return  new_state, reward, done, None
            
    def __calculate_reward(self, action, new_state, player):
        if self.__check_if_game_over(player):
            print('30')
            return 30
        elif action in [0, 1, 2, 3, 4]:
            if self.__check_collision(action, new_state):
                print('-6')
                return -6
            elif action == 4:
                print('0')
                return 0
            else:
                print('2')
                return 2
        elif action == 5:
            if self.__check_for_bomb(action, new_state):
                print('5')
                return 5
            else:
                print('-5')
                return -5
            
    def __check_for_bomb(self, action, state):
        if state[1] == 2:
            return True
        elif state[3] == 2:
            return True
        elif state[5] == 2:
            return True
        elif state[7] == 2:
            return True
        return False
        
    def __check_collision(self, action, state):
        if action == 0 and state[3] in [1, 2]:
            return True
        elif action == 1 and state[5] in [1, 2]:
            return True
        elif action == 2 and state[1] in [1, 2]:
            return True
        elif action == 3 and state[7]in [1, 2]:
            return True
        return False
        
    def __check_if_game_over(self, player):
        # if player.get_position() == (6, 4):
        #     return True
        # return False
        if player._current_state == player.states['Dying']:
            return True
        return False
    
    def __create_map(self) -> None:
        x1, y1 = 0.062 * self.__width, 0.11 * self.__height
        x2, y2 = 0.941 * self.__width, 0.11 * self.__height
        width = x2 - x1
        tile_width = width / self._columns
        x3, y3 = 0.941 * self.__width, 0.11 * self.__height
        x4, y4 = 0.941 * self.__width, 0.87 * self.__height
        height = y4 - y3
        tile_height = height / self._rows
        
        current_row = []
        for i in range(self._rows):
            for j in range(self._columns):
                current_row.append(Tile(x1 + j * tile_width, y1 + i * tile_height, tile_width))
            self.origin_map.append(current_row)
            current_row = []
                    
        # for i in range(self._columns):
        #     for j in range(self._rows):
        #         if (i == 0 and j == 0) or (i == self._columns - 1 and j == 0) or (i == 0 and j == self._rows - 1) or (i == self._columns - 1 and j == self._rows - 1):
        #             continue
        #         if i % 2 == 0 and j % 2 == 0:
        #             self.origin_map[j][i] = Wall(self.origin_map[j][i].x, self.origin_map[j][i].y, tile_width, tile_height)
                    
        # n_crates = int(len(self.origin_map[0]) * 1) * self._rows
        n_crates = 100
        
        for i in range(n_crates):
            x = random.randint(0, self._columns - 1)
            y = random.randint(0, self._rows - 1)
            if (0 <= x <= 1 or self._columns - 2 <= x <= self._columns - 1) and (0 <= y <= 1 or self._rows - 2 <= y <= self._rows - 1):
                continue
            elif not isinstance(self.origin_map[y][x], Wall):
                self.origin_map[y][x] = Crate(self.origin_map[y][x].x, self.origin_map[y][x].y, tile_width, tile_height)
        
    def set_starting_postion(self, x: int, y: int) -> tuple:
        return (self.origin_map[x][y].x, self.origin_map[x][y].y)
    
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
    
    def render_map(self, game_display: pygame.display, delta_time) -> None:
        game_display.blit(self.__current_background, (0, 0))
        
        for row in self.current_map:
            for tile in row:
                if isinstance(tile, Wall) or isinstance(tile, Crate):
                    game_display.blit(tile.image, (tile.rect.x, tile.rect.y))
        
        self.bombs.update(delta_time)

        # position = self.__players[0].get_position()
        # if position is not None:
        #     x, y = position
        #     self.get_map_state((x, y))
        # else:
            
        #     print("Pozice hráče nebyla nalezena")
                    
        # for row in self.current_map:
        #     for tile in row:
        #         pygame.draw.rect(game_display, BLUE, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height), 2)
                    
    def __check_explosion_direction(self, x: int, y: int, radius: int, explosion_tiles: list, direction_x: int, direction_y: int):
        for k in range(1, radius + 1):
            new_x, new_y = x + k * direction_x, y + k * direction_y
            if 0 <= new_x < len(self.current_map) and 0 <= new_y < len(self.current_map[new_x]):
                tile = self.current_map[new_x][new_y]
                if isinstance(tile, Wall):
                    break
                elif isinstance(tile, Crate) or isinstance(tile, Tile):
                    explosion_tiles.append((tile, new_x, new_y))
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
                        self.current_map[x][y] = Tile(tile.rect.x, tile.rect.y, tile.rect.width)
   
    def update(self, object) -> None:
        if isinstance(object, Bomb):
            explosion_tiles = {'up': [], 'down': [], 'left': [], 'right': [], 'center': []}
            for row in list(self.current_map):
                for tile in list(row):
                    if tile == object:
                        x = self.current_map.index(row)
                        y = row.index(tile)
                        explosion_tiles['center'].append((tile, x, y))
                        self.__check_explosion_direction(x, y, tile.explosion_radius, explosion_tiles['left'], 0, -1)
                        self.__check_explosion_direction(x, y, tile.explosion_radius, explosion_tiles['right'], 0, 1)
                        self.__check_explosion_direction(x, y, tile.explosion_radius, explosion_tiles['up'], -1, 0)
                        self.__check_explosion_direction(x, y, tile.explosion_radius, explosion_tiles['down'], 1, 0)
                        object.set_explosion(explosion_tiles)
                        self.__check_player_position(explosion_tiles)
                        self.__destroy_crates(explosion_tiles)
                        row[y] = Tile(tile.rect.x, tile.rect.y, tile.rect.width)