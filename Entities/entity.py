import pygame
from Utilities.sprite_loader import load
from pygame.math import Vector2

class Entity():
    def __init__(self, x: int, y: int, entity_name: str) -> None:
        self._x = x
        self._y = y
        self._all_actions = load(entity_name)
        self._direction = Vector2(0, 0)
        
    def _move_left(self) -> None:
        self._direction.x = -1
        
    def _move_right(self) -> None:
        self._direction.x = 1
        
    def _move_up(self) -> None:
        self._direction.y = -1
    
    def _move_down(self) -> None:
        self._direction.y = 1
        
    def update(self) -> None:
        pass