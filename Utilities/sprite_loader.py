import pygame
import os
from Utilities.colors import Colors

def load(directory: str) -> dict:
    def get_sprites(file_path: str, frames: int, width: int, height: int, scale: float) -> list:
        all_sprites = []
        sprite_sheet = pygame.image.load(file_path).convert_alpha()
        for i in range(frames):
            image = pygame.Surface((width, height)).convert_alpha()
            image.blit(sprite_sheet, (0, 0), ((i * width), 0, width, height))
            image = pygame.transform.scale(image, (width * scale, height * scale))
            image.set_colorkey(Colors.BLACK)
            all_sprites.append(image)
            
        return all_sprites
    
    all_actions_dictionary = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(current_dir, '..')
    to_load_dir = os.path.join(root_dir, 'Assets', directory)
    
    for sub_directory in os.listdir(to_load_dir):
        all_actions_dictionary[sub_directory] = {}
        for image in os.listdir(f'{to_load_dir}/{sub_directory}'):
            all_actions_dictionary[sub_directory][image.split('.')[0]] = get_sprites(f'{to_load_dir}/{sub_directory}/{image}', 4, 32, 34, 3)
            
    return all_actions_dictionary