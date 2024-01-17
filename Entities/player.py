import pygame
from pygame.math import Vector2
from Utilities.sprite_loader import load

class Player():
    def __init__(self):
        self.__all_actions = load('player_character')
        self.__x = 0
        self.__y = 0
        self.__direction = Vector2(0,0)
        
    def update(self, screen: pygame.display):
        screen.blit(self.__all_actions['Idle']['front'][0], (0, 0))
        