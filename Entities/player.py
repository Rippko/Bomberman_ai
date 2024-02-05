import pygame
from pygame.math import Vector2
from Entities.entity import Entity
from bomb import Bomb
from Utilities.colors import Colors

class Player(Entity):
    def __init__(self, x, y, entity_name, n_frames: int, s_width: int, s_height: int, scale) -> None:
        super().__init__(x, y, entity_name, n_frames, s_width, s_height, scale)
        self._movement_speed = 5
        self.__bombs = pygame.sprite.Group()
        
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
            
        if pressed_keys[pygame.K_SPACE] and len(self.__bombs) < 1:
            self.__place_bomb()
            
    def __handle_horizontal_collisions(self, collided: bool) -> None:
        if collided: self._direction.x = 0
        
    def __handle_vertical_collisions(self, collided: bool) -> None:
        if collided: self._direction.y = 0
        
    def __place_bomb(self):
        self.__bombs.add(Bomb(self._x, self._y))
        
    
    def update(self, game_display: pygame.display, pressed_keys, collidables: list[pygame.Rect]) -> None:
        self.__check_keys(pressed_keys)

        self.__bombs.draw(game_display)
        self.__bombs.update()
        
        self._move_horizontal()
        self.__handle_horizontal_collisions(self._horizontal_collisions(collidables))
        
        self._move_vertical()
        self.__handle_vertical_collisions(self._vertical_collisions(collidables))
        
        pygame.draw.rect(game_display, Colors.GREEN, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
        
        super().update(game_display)