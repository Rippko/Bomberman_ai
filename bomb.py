import pygame
from Utilities.settings import *
from Utilities.sprite_loader import load
from Utilities.observable_object import ObservableObject
from Obstacles.crate import Crate

class Bomb(pygame.sprite.Sprite, ObservableObject):
    def __init__(self, x: int, y: int, game_display: pygame.display) -> None:
        pygame.sprite.Sprite.__init__(self)
        ObservableObject.__init__(self)
        self.__x = x
        self.__y = y
        self.__game_display = game_display
        self.images = []
        for i in range(0, 12):
            if i < 10:
                self.images.append(pygame.image.load(f'Assets/Bomb/00{i}.png').convert_alpha())
                self.images[i] = pygame.transform.scale(self.images[i], (70, 70))
            else:
                self.images.append(pygame.image.load(f'Assets/Bomb/0{i}.png').convert_alpha())
                self.images[i] = pygame.transform.scale(self.images[i], (70, 70))
        
        self.explosion_images = load('Explosions', 12, 120, 120, 0.58)
        
        self.__last_update = pygame.time.get_ticks()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(self.__x, self.__y))
        self.explosion_radius = 2
        self.__animation_speed = 90
        self.__exploded = False
        self.__directions = {}
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)
    
    def __explode(self) -> None:
        self.notify_observers()
        
    def set_explosion(self, explosion_tiles: dict) -> None:
        self.__exploded = True
        self.__directions = explosion_tiles
        
    def __check_direction(self, direction: str, image: pygame.Surface) -> pygame.Surface:
        match direction:
            case 'up':
                return pygame.transform.rotate(image, 90).convert_alpha()
            case 'down':
                return pygame.transform.rotate(image, 90).convert_alpha()
            case 'left':
                return image
            case 'right':
                return image
        
    def update(self) -> None:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.__last_update
        
        if not self.__exploded:
            current_image = self.images[self.index]
            
            self.__game_display.blit(current_image, (self.__x, self.__y))
            
            if delta_time >= self.__animation_speed:
                if self.index < len(self.images) - 1:
                    self.index += 1

                if self.index >= len(self.images) - 1:
                    self.index = 0
                    self.__explode()
                    
                self.__last_update = current_time
        else:
            for key in self.__directions:
                for tile, x, y in self.__directions[key]:
                    if not isinstance(tile, Crate):
                        self.__game_display.blit(self.explosion_images['center'][self.index], (self.rect.x, self.rect.y))
                        self.__game_display.blit(self.__check_direction(key, self.explosion_images['middle'][self.index]), (tile.rect.x, tile.rect.y))
                    
            if delta_time >= self.__animation_speed:
                if self.index < len(self.explosion_images['middle']) - 1:
                    self.index += 1
                else:
                    self.kill()
                    
                self.__last_update = current_time