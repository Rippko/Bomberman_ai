import pygame
from Utilities.sprite_loader import load
from pygame.math import Vector2
from States.Entity.idling_state import IdlingState
from States.Entity.walking_state import WalkingState
from States.Entity.dying_state import DyingState
from Utilities.settings import *

class Entity():
    def __init__(self, x: int, y: int, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale) -> None:
        self._x = x
        self._y = y
        self._all_actions = load(entity_name, n_frames, s_width, s_height, scale)
        self._direction = Vector2(0, 0)
        self._current_delta_time = 0
        self._animation_speed = 0.1
        self._current_frame = 0
        self._current_state = IdlingState('Idle')
        
        self.states = {'Idle': IdlingState('Idle'), 'Walking': WalkingState('Walking'), 'Dying': DyingState('Dying')}
        
        self.image = self._all_actions['Idle']['front'][0]
        
        self.__shrink_width = 25
        self.__shrink_height = 30
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-self.__shrink_width, -self.__shrink_height)

        self._movement_speed = 3
        
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
        latest_state = self.states[self._current_state.handle_event(keys)]
        if not self._current_state == latest_state:
            self._current_state = latest_state
            self._current_frame = 0
        
    def set_dead(self) -> None:
        if not self._current_state == self.states['Dying']:
            self._direction = Vector2(0, 0)
            self._current_frame = 0
            self._current_state = self.states['Dying']
        
    def _animate(self, game_display: pygame.display, delta_time):
        self._current_delta_time += delta_time
         
        if self._current_delta_time >= self._animation_speed:
            if self._current_frame < len(self._all_actions[self._current_state.get_name()][self._get_direction()]) - 1:
                self._current_frame += 1
            elif self._current_state.get_name() == 'Dying':
                self._current_frame = len(self._all_actions[self._current_state.get_name()]['front']) - 1
            else:
                self._current_frame = 0
                
            self._current_delta_time = 0
        
        current_image = self._all_actions[self._current_state.get_name()][self._get_direction()][self._current_frame]
        
        game_display.blit(current_image, (self._x, self._y))
            
    def _move_horizontal(self):
        self._x += self._direction.x * self._movement_speed
        self.rect.x = self._x + (self.__shrink_width // 2)
      
    def _horizontal_collisions(self, collidables) -> bool:
        collided = False
        
        for tile in collidables:
            if tile.colliderect(self.rect):
                if self._direction.x < 0:
                    self.rect.left = tile.right
                    self._x = self.rect.x - (self.__shrink_width // 2)
                            
                elif self._direction.x > 0:
                    self.rect.right = tile.left
                    self._x = self.rect.x - (self.__shrink_width // 2)
                    
                collided = True
            
        return collided
    
    def _move_vertical(self):
        self._y += self._direction.y * self._movement_speed
        self.rect.y = self._y + self.__shrink_height
    
    def _vertical_collisions(self, collidables) -> bool:
        collided = False
        
        for tile in collidables:
            if tile.colliderect(self.rect):
                if self._direction.y > 0:
                    self.rect.bottom = tile.top
                    self._y = self.rect.y - self.__shrink_height
                elif self._direction.y < 0:
                    self.rect.top = tile.bottom
                    self._y = self.rect.y - self.__shrink_height
                collided = True
        return collided
    
    def update(self, game_display: pygame.display, delta_time) -> None:
        self._animate(game_display, delta_time)
        