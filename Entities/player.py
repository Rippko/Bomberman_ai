import pygame
from pygame.math import Vector2
from Utilities.sprite_loader import load

class Player():
    def __init__(self, x, y):
        self.__all_actions = load('player_character')
        self.__x = x
        self.__y = y
        self.__direction = Vector2(0,0)
        self.__movement_speed = 7
        
    def __move_left(self) -> None:
        self.__direction.x = -1
        
    def __move_right(self) -> None:
        self.__direction.x = 1
        
    def __move_up(self) -> None:
        self.__direction.y = -1
    
    def __move_down(self) -> None:
        self.__direction.y = 1
        
    def __check_keys(self):
        self.__direction = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.__move_left()
        if keys[pygame.K_d]:
            self.__move_right()
        if keys[pygame.K_w]:
            self.__move_up()
        if keys[pygame.K_s]:
            self.__move_down()
    
    def update(self, screen: pygame.display):
        self.__check_keys()
        self.__x += self.__direction.x * self.__movement_speed
        self.__y += self.__direction.y * self.__movement_speed
        
        screen.blit(self.__all_actions['Idle']['front'][0], (self.__x, self.__y))
        