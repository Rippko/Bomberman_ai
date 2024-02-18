import pygame
from States.state import State

class WalkingState(State):
    def __init__(self, name) -> None:
        super().__init__(name)
        
    def handle_event(self, keys) -> None:
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            return self._name
        else:
            return 'Idle'
            