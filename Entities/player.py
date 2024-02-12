import pygame
from pygame.math import Vector2
from Entities.entity import Entity
from bomb import Bomb
from Utilities.settings import *

class Player(Entity):
    def __init__(self, coords: tuple, entity_name: str, n_frames: int, s_width: int, s_height: int, scale, grid: list) -> None:
        super().__init__(coords[0], coords[1], entity_name, n_frames, s_width, s_height, scale)
        self._movement_speed = 5
        self.__grid = grid
        self.__bombs = pygame.sprite.Group()
        
        
    def __check_keys(self, pressed_keys) -> None:
        self._direction = Vector2(0, 0)
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self._move_left()
        elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self._move_right()
        elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self._move_up()
        elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self._move_down()
            
        if pressed_keys[pygame.K_SPACE] and len(self.__bombs) < 1:
            self.__place_bomb()
            
    def __handle_horizontal_collisions(self, collided: bool) -> None:
        if collided: self._direction.x = 0
        
    def __handle_vertical_collisions(self, collided: bool) -> None:
        if collided: self._direction.y = 0
        
    def __place_bomb(self):
        for row in self.__grid:
            for tile in row:
                if int(self.rect.centerx) in range(int(tile.rect.x), int(tile.rect.x) + int(tile.rect.width)) and int(self.rect.centery) in range(int(tile.rect.y), int(tile.rect.y) + int(tile.rect.height)):
                    self.__bombs.add(Bomb(tile.rect.x, tile.rect.y))
                    return
    
    def update(self, game_display: pygame.display, pressed_keys) -> None:
        self.__check_keys(pressed_keys)
        collidables = [tile.rect for row in self.__grid for tile in row if not tile.isEmpty]

        for bomb in self.__bombs:
            if self.rect.colliderect(bomb.rect):
                continue
            else:
                collidables.append(bomb.rect)

        self.__bombs.update(game_display)
        
        self._move_horizontal()
        self.__handle_horizontal_collisions(self._horizontal_collisions(collidables))
        
        self._move_vertical()
        self.__handle_vertical_collisions(self._vertical_collisions(collidables))

        #pygame.draw.rect(game_display, GREEN, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
        
        super().update(game_display)