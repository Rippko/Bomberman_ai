import pygame
from pygame.math import Vector2
from Utilities.sprite_loader import load
from Entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y, entity_name):
        super().__init__(x, y, entity_name)
        self.__movement_speed = 7
        
    def __check_keys(self):
        self._direction = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self._move_left()
        if keys[pygame.K_d]:
            self._move_right()
        if keys[pygame.K_w]:
            self._move_up()
        if keys[pygame.K_s]:
            self._move_down()
    
    def update(self, screen: pygame.display):
        super().update()
        
        self.__check_keys()
        self._x += self._direction.x * self.__movement_speed
        self._y += self._direction.y * self.__movement_speed
        
        screen.blit(self._all_actions['Idle']['front'][0], (self._x, self._y))
        