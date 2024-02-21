import pygame
from States.state import State

class DyingState(State):
    def __init__(self, name) -> None:
        super().__init__(name)
        
    def handle_event(self, keys) -> str:
        return self._name