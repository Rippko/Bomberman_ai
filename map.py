import pygame
from Obstacles.tile import Tile
from Obstacles.wall import Wall
from Obstacles.crate import Crate
from bomb import Bomb
from Utilities.settings import *
from Utilities.asset_loader import AssetLoader
from Utilities.observer import Observer
from enum import Enum
import random
import math

class Action(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_UP = 2
    MOVE_DOWN = 3
    STOP_MOVE = 4
    PLACE_BOMB = 5

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
        self.tile_height = self.origin_map[0][0].rect.height
        self.map_size = self.calculate_game_plan_size()
        self.__current_w = self.__width
        self.__current_h = self.__height
        
        self.max_explosion_radius = 2
        
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
        
    def get_map_state(self, player):
        local_map_vector = []
        player_position = player._get_position_in_grid(player.x, player.y)
        if player_position is not None:
            x, y = player_position
            directions = [(-1, 0), (-2, 0), (1, 0), (2, 0), (0, -1), (0, -2), (0, 1), (0, 2)] # left, right, up, down
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.current_map[0]) and 0 <= ny < len(self.current_map):
                    tile = self.current_map[ny][nx]
                    if type(tile) == Tile:
                        is_player = False
                        for p in self.__players:
                            if p.check_position(tile):
                                is_player = True
                                break
                        if is_player:
                            local_map_vector.append(4)
                        else:
                            local_map_vector.append(0)
                    elif type(tile) == Wall:
                        local_map_vector.append(1)
                    elif type(tile) == Crate:
                        local_map_vector.append(2)
                    elif type(tile) == Bomb:
                        local_map_vector.append(3)
                else:
                    local_map_vector.append(1)

            in_danger = self.is_in_explosion_range((x, y))
            local_map_vector.append(in_danger)
            
            player_position = self.get_nearest_player(player)
            local_map_vector.append(player_position)
            
            return tuple(local_map_vector)
        return None
    
    def get_nearest_player(self, player):
        nearest_player = None
        nearest_distance = float('inf')
        for p in self.__players:
            if p != player and p._current_state != p.states['Dying']:
                distance = math.dist([player.x, player.y], [p.x, p.y])
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_player = p
        
        if nearest_player is not None:
            distance_x = abs(player.x - nearest_player.x)
            distance_y = abs(player.y - nearest_player.y)
            if distance_x > distance_y:
                return 'player_on_left' if player.x >= nearest_player.x else 'player_on_right'
            else:
                return 'player_on_top' if player.y >= nearest_player.y else 'player_on_bottom'
        return 'no_player'
        
    def is_in_explosion_range(self, position):
        x, y = position
        directions = {
            'center': (0, 0), 'left': (-1, 0), 'right': (1, 0),
            'up': (0, -1), 'down': (0, 1), 'top_left': (-1, -1),
            'top_right': (1, -1), 'bottom_left': (-1, 1), 'bottom_right': (1, 1)
        }
        extended_directions = {
            'far_left': (-2, 0), 'far_right': (2, 0), 'far_up': (0, -2), 'far_down': (0, 2)
        }
        for name, (dx, dy) in {**directions, **extended_directions}.items():
            distance_max = 1 if name in directions else 2
            for distance in range(0, distance_max + 1):
                nx, ny = x + dx * distance, y + dy * distance
                if not (0 <= nx < len(self.current_map[0]) and 0 <= ny < len(self.current_map)):
                    break
                tile = self.current_map[ny][nx]
                if isinstance(tile, Wall):
                    break
                if isinstance(tile, Bomb) and distance <= tile.explosion_radius:
                    return f'bomb_{name}'
        return 'safe'
    
    def step(self, action, state, player):
        if player is None:
            return
        else:
            if action == Action.PLACE_BOMB:
                player.action_map[Action.STOP_MOVE]()
                player.action_map[action]()
            else:
                player.action_map[action]()
                
            reward = self.__calculate_reward(action, state, player)
            new_state = self.get_map_state(player)
            done  = self.__check_if_game_over(player)
            return  new_state, reward, done, None
            
    def __calculate_reward(self, action, state, player):
        reward = 0
        if self.__check_if_game_over(player):
            print('-100 because game over')
            reward += -100
        elif action in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_UP, Action.MOVE_DOWN]:
            if self.__check_collision(action, state) and state[8] == 'safe':
                print('-10 because went into wall or crate')
                reward += -10
            elif state[8] != 'safe':
                reward += self.__check_bomb_reward(action, state)
            else:
                if self.__walk_towards_player(action, state):
                    print('5 because walking towards player')
                    reward += 5
                else:
                    print('2 because moving on tile')
                    reward += 2
        elif action == Action.STOP_MOVE:
            if state[8] in ['bomb_left', 'bomb_right', 'bomb_up', 'bomb_down']:
                print('-20 because standing still and bomb is near')
                reward += -20
            else:
                print('-2 because standing still')
                reward += -2
        elif action == Action.PLACE_BOMB:
            if state[8] == 'safe':
                if 2 in [state[0], state[2], state[4], state[6]] or 4 in [state[0], state[2], state[4], state[6]]:
                    print('30 because placing bomb next to crate or player')
                    reward += 30
                else:
                    print('-30 because placing bomb without any crate nearby')
                    reward += -30
        return reward
    
    def __walk_towards_player(self, action: Action, state) -> bool:
        if action == Action.MOVE_LEFT and state[9] == 'player_on_left':
            return True
        elif action == Action.MOVE_RIGHT and state[9] == 'player_on_right':
            return True
        elif action == Action.MOVE_UP and state[9] == 'player_on_top':
            return True
        elif action == Action.MOVE_DOWN and state[9] == 'player_on_bottom':
            return True
        return False
        
    def __check_bomb_reward(self, action: Action, state):
        danger_mapping = {
            Action.MOVE_LEFT: ['bomb_left', 'bomb_far_left', 'bomb_top_left', 'bomb_bottom_left'],
            Action.MOVE_RIGHT: ['bomb_right', 'bomb_far_right', 'bomb_top_right', 'bomb_bottom_right'],
            Action.MOVE_UP: ['bomb_up', 'bomb_far_up', 'bomb_top_left', 'bomb_top_right'],
            Action.MOVE_DOWN: ['bomb_down', 'bomb_far_down', 'bomb_bottom_left', 'bomb_bottom_right']
        }
        bomb_positions = danger_mapping.get(action, [])
        if state[8] in bomb_positions:
            print(f'-20 because bomb is in direction of {state[4]}')
            return -20
        else:
            if self.__check_collision(action, state):
                print('-30 because went into wall while bomb is near')
                return -30
            else:
                return self.__get_correct_escape_direction(action, state)
            
    def __get_correct_escape_direction(self, action, state):
        if action == Action.MOVE_LEFT and state[0] == 0 and state[1] == 0:
            print('30 because moving away from bomb')
            return 30
        elif action == Action.MOVE_RIGHT and state[2] == 0 and state[3] == 0:
            print('30 because moving away from bomb')
            return 30
        elif action == Action.MOVE_UP and state[4] == 0 and state[5] == 0:
            print('30 because moving away from bomb')
            return 30
        elif action == Action.MOVE_DOWN and state[6] == 0 and state[7] == 0:
            print('30 because moving away from bomb')
            return 30
        else:
            print('-10 because went into false escape direction')
            return -10         
        
    def __check_collision(self, action, state):
        if action == Action.MOVE_LEFT and state[0] in [1, 2, 3]:
            return True
        elif action == Action.MOVE_RIGHT and state[2] in [1, 2, 3]:
            return True
        elif action == Action.MOVE_DOWN and state[6] in [1, 2, 3]:
            return True
        elif action == Action.MOVE_UP and state[4] in [1, 2, 3]:
            return True
        return False
        
    def __check_if_game_over(self, player):
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
                    
        for i in range(self._columns):
            for j in range(self._rows):
                if (i == 0 and j == 0) or (i == self._columns - 1 and j == 0) or (i == 0 and j == self._rows - 1) or (i == self._columns - 1 and j == self._rows - 1):
                    continue
                if i % 2 == 0 and j % 2 == 0:
                    self.origin_map[j][i] = Wall(self.origin_map[j][i].x, self.origin_map[j][i].y, tile_width, tile_height)
                    
        # n_crates = len(self.origin_map[0]) * self._rows
        n_crates = 150
        
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