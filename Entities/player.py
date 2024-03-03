import pygame
from pygame.math import Vector2
from Entities.entity import Entity
from Obstacles.wall import Wall
from Obstacles.crate import Crate
from bomb import Bomb
from Utilities.settings import *
from Utilities.observable_object import ObservableObject
from map import Map

class Player(Entity):
    def __init__(self, coords: tuple, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale, map: Map, game_display: pygame.display) -> None:
        super().__init__(coords[0], coords[1], entity_name, n_frames, s_width, s_height, scale)
        self.__game_display = game_display
        self._movement_speed = 5
        self.__map = map
        self.__grid = self.__map.current_map
        self.__bombs = pygame.sprite.Group()
        self.__max_bombs = 2
        self.__bomb_strength = 1
        
        self.__map_size = self.__map.calculate_game_plan_size()
        
    def __check_keys(self, pressed_keys) -> None:
        self._direction = Vector2(0, 0)
        
        self.handle_keypress(pressed_keys)
        if (pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]) and self.rect.x > self.__map_size[0]:
            self._move_left()
        elif (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]) and self.rect.x < (self.__map_size[1] - self.rect.width):
            self._move_right()
        elif (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]) and self.rect.y > self.__map_size[2]:
            self._move_up()
        elif (pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]) and self.rect.y < (self.__map_size[3] - self.rect.height - 5):
            self._move_down()
                
        if pressed_keys[pygame.K_SPACE] and len(self.__bombs) < self.__max_bombs:
            self.__place_bomb()
            
    def __handle_horizontal_collisions(self, collided: bool) -> None:
        if collided: self._direction.x = 0
        
    def __handle_vertical_collisions(self, collided: bool) -> None:
        if collided: self._direction.y = 0
        
    def check_position(self, tile) -> bool:
        return int(self.rect.centerx) in range(int(tile.rect.x), int(tile.rect.x) + int(tile.rect.width)) and int(self.rect.centery) in range(int(tile.rect.y), int(tile.rect.y) + int(tile.rect.height))
    
    def __place_bomb(self) -> None:
        for row in self.__grid:
            for tile in row:
                if self.check_position(tile) and not isinstance(tile, Bomb):
                    bomb = Bomb(tile.rect.x, tile.rect.y, self.__bomb_strength, self.__game_display)
                    bomb.add_observer(self.__map)
                    self.__bombs.add(bomb)
                    self.__grid[self.__grid.index(row)][row.index(tile)] = bomb
                    return
    
    def update(self, pressed_keys, delta_time) -> None:
        collidables = [tile.rect for row in self.__grid for tile in row if isinstance(tile, Wall) or isinstance(tile, Crate)]
        if not self._current_state == self.states['Dying']:
            self.__check_keys(pressed_keys)
            for bomb in self.__bombs:
                if self.rect.colliderect(bomb.rect):
                    continue
                else:
                    collidables.append(bomb.rect)

            self.__bombs.update(delta_time)
            
            self._move_horizontal()
            self.__handle_horizontal_collisions(self._horizontal_collisions(collidables))
            
            self._move_vertical()
            self.__handle_vertical_collisions(self._vertical_collisions(collidables))

            #pygame.draw.rect(game_display, GREEN, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
            
            super().update(self.__game_display, delta_time)
            
        else:
            for bomb in self.__bombs:
                if self.rect.colliderect(bomb.rect):
                    continue
                else:
                    collidables.append(bomb.rect)

            self.__bombs.update(delta_time)
            
            super().update(self.__game_display, delta_time)