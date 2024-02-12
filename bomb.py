import pygame
from Utilities.settings import *
from Utilities.sprite_loader import load

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__x = x
        self.__y = y
        self.images = []
        for i in range(0, 11):
            if i < 10:
                self.images.append(pygame.image.load(f'Assets/Bomb/00{i}.png').convert_alpha())
                self.images[i] = pygame.transform.scale(self.images[i], (70, 70))
            else:
                self.images.append(pygame.image.load(f'Assets/Bomb/0{i}.png').convert_alpha())
                self.images[i] = pygame.transform.scale(self.images[i], (70, 70))
        
        self.__explosion_images = load('Explosions', 15, 120, 120, 0.5)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(self.__x, self.__y))
        self.__explosion_radius = 1
        self.__bomb_timer = 7
        self.__counter = 0
        
    def __explode(self):
        pass
    
    def draw(self, game_display: pygame.display) -> None:
        game_display.blit(self.image, (self.__x, self.__y))
        
        
    def update(self, game_display: pygame.display) -> None:        
        self.__counter += 1
        if self.__counter >= self.__bomb_timer and self.index < len(self.images) - 1:
            self.__counter = 0
            self.index += 1
            self.image = self.images[self.index]
            
        self.draw(game_display)
        
        if self.index >= len(self.images) - 1 and self.__counter >= self.__bomb_timer:
            
            for i in range(1, self.__explosion_radius + 1):
                self.__explode()
            self.kill()