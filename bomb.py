import pygame

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
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(self.__x, self.__y))
        self.__explosion_radius = 1
        self.__bomb_timer = 9
        self.__counter = 0
        
    def update(self):
        self.__counter += 1
        if self.__counter >= self.__bomb_timer and self.index < len(self.images) - 1:
            self.__counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.__counter >= self.__bomb_timer:
            self.kill()