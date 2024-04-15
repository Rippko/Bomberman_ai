import pygame
from States.Entity.state import State

class DyingState(State):
    def __init__(self, name) -> None:
        super().__init__(name)
        
    def handle_event(self, direction: pygame.math.Vector2) -> str:
        return self._name