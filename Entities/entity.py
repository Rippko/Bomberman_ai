import pygame
from Utilities.sprite_loader import load
from pygame.math import Vector2
from States.Entity.idling_state import IdlingState
from States.Entity.walking_state import WalkingState

class Entity():
    def __init__(self, x: int, y: int, entity_name: str) -> None:
        self._x = x
        self._y = y
        self._all_actions = load(entity_name)
        self._direction = Vector2(0, 0)
        self._last_update = pygame.time.get_ticks()
        self._animation_speed = 150
        self._current_frame = 0
        self._current_state = IdlingState('Idle')
        
        self.states = {'Idle': IdlingState('Idle'),
                       'Walking': WalkingState('Walking')
                       }
        
    def _move_left(self) -> None:
        self._direction.x = -1
        
    def _move_right(self) -> None:
        self._direction.x = 1
        
    def _move_up(self) -> None:
        self._direction.y = -1
    
    def _move_down(self) -> None:
        self._direction.y = 1
    
    def _get_direction(self) -> str:
        if self._direction.x > 0:
            return 'right'
        elif self._direction.x < 0:
            return 'left'
        elif self._direction.y > 0:
            return 'front'
        elif self._direction.y < 0:
            return 'back'
        else:
            return 'front'
        
    def handle_keypress(self, keys) -> None:
        self._current_state = self.states[self._current_state.handle_event(keys)]
        print(self._current_state.get_name())
        
    def _animate(self, game_display: pygame.display):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self._last_update
        
        current_image = self._all_actions[self._current_state.get_name()][self._get_direction()][self._current_frame]
        
        game_display.blit(current_image, (self._x, self._y))
        
        if delta_time >= self._animation_speed:
            if self._current_frame < len(self._all_actions[self._current_state.get_name()][self._get_direction()]) - 1:
                self._current_frame += 1
            else:
                self._current_frame = 0
        
            self._last_update = current_time
        
    def update(self, game_display: pygame.display) -> None:
        self._animate(game_display)