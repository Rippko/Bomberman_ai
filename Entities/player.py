import pygame

class Player():
    sprite_sheet = None
    single_sprites = []
    __BLACK = (0, 0, 0)
    def __init__(self):
        self.all_actions = {}
        self.load_sprite_sheets()
        for i in range(4):
            self.single_sprites.append(self.get_sprites(i, 32, 33, 3))
            print(i)
        
    def load_sprite_sheets(self):
        self.sprite_sheet = pygame.image.load('player_character/idle-front.png').convert_alpha()
        
    def get_sprites(self, frame, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(self.__BLACK)
        
        return image