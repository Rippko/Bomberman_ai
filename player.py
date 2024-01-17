import pygame

class Player():
    sprite_sheet = None
    single_images = []
    __BLACK = (0, 0, 0)
    def __init__(self):
        self.load_sprite_sheets()
        for i in range(4):
            self.single_images.append(self.get_sprites(i, 32, 33, 3))
            print(i)
        
    def load_sprite_sheets(self):
        self.sprite_sheet = pygame.image.load('player_character/idle-front.png').convert_alpha()
        
    def get_sprites(self, frame, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        #image.set_colorkey(self.__BLACK)
        
        return image