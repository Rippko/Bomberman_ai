import pygame
from Utilities.sprite_loader import load
from pygame.math import Vector2
from States.Entity.idling_state import IdlingState
from States.Entity.walking_state import WalkingState
from Utilities.colors import Colors

class Entity():
    def __init__(self, x: int, y: int, entity_name: str, n_frames: int, s_width: int, s_height: int, scale) -> None:
        self._x = x
        self._y = y
        self._all_actions = load(entity_name, n_frames, s_width, s_height, scale)
        self._direction = Vector2(0, 0)
        self._last_update = pygame.time.get_ticks()
        self._animation_speed = 150
        self._current_frame = 0
        self._current_state = IdlingState('Idle')
        
        self.states = {'Idle': IdlingState('Idle'),
                       'Walking': WalkingState('Walking')
                       }
        
        self._rect = self._all_actions['Idle']['front'][0].get_rect(center=(x,y))
        
        self._movement_speed = 5
        
        
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
          
    def _move_horizontal(self):
        self._x += self._direction.x * self._movement_speed
        self._rect.x = self._x        
      
    def _horizontal_collisions(self, collidables) -> bool:
        collided = False
        
        for tile in collidables:
            if tile.colliderect(self._rect):
                if self._direction.x < 0:
                    self._rect.left = tile.right
                    self._x = self._rect.x
                    # else:
                    #     self._move_right()
                            
                elif self._direction.x > 0:
                    self._rect.right = tile.left
                    self._x = self._rect.x
                    # else:
                    #     self._move_left()
                collided = True
            
        return collided
    
    def _move_vertical(self):
        self._y += self._direction.y * self._movement_speed
        self._rect.y = self._y 
    
    def _vertical_collisions(self, collidables) -> bool:
        collided = False
        for tile in collidables:
            if tile.colliderect(self._rect):
                if self._direction.y > 0:
                    self._rect.bottom = tile.top
                    self._y = self._rect.y
                elif self._direction.y < 0:
                    self._rect.top = tile.bottom
                    self._y = self._rect.y
                collided = True
        return collided
    
    def update(self, game_display: pygame.display) -> None:
        self._animate(game_display)
        