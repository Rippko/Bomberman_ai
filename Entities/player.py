import pygame
from pygame.math import Vector2
from Utilities.sprite_loader import load
from Entities.entity import Entity
from Utilities.colors import Colors

class Player(Entity):
    def __init__(self, x, y, entity_name, n_frames: int, s_width: int, s_height: int, scale) -> None:
        super().__init__(x, y, entity_name, n_frames, s_width, s_height, scale)
        self._movement_speed = 7
        
    def __check_keys(self, pressed_keys) -> None:
        self._direction = Vector2(0, 0)
        if pressed_keys[pygame.K_a]:
            self._move_left()
        elif pressed_keys[pygame.K_d]:
            self._move_right()
        elif pressed_keys[pygame.K_w]:
            self._move_up()
        elif pressed_keys[pygame.K_s]:
            self._move_down()
            
    def __handle_horizontal_collisions(self, collided: bool) -> None:
        if collided: self._direction.x = 0
        
    def __handle_vertical_collisions(self, collided: bool) -> None:
        if collided: self._direction.y = 0
    
    def update(self, screen: pygame.display, pressed_keys, collidables: list[pygame.Rect]) -> None:
        self.__check_keys(pressed_keys)
        
        self._move_horizontal()
        self.__handle_horizontal_collisions(self._horizontal_collisions(collidables))
        
        self._move_vertical()
        self.__handle_vertical_collisions(self._vertical_collisions(collidables))
        
        pygame.draw.rect(screen, Colors.GREEN, (self._rect.x, self._rect.y, self._rect.w, self._rect.h))
        super().update(screen)