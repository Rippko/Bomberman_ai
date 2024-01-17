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
    
    # We need to get the right directory in our file system to load all sprites from which is App/Assets/directory
    asset_directory = os.path.join((os.path.dirname(os.path.abspath(__file__))), '..', 'Assets', directory)

    all_actions_dictionary = {}
    for sub_directory in os.listdir(asset_directory):
        all_actions_dictionary[sub_directory] = {}
        for image in os.listdir(f'{asset_directory}/{sub_directory}'):
            current_image_path = f'{asset_directory}/{sub_directory}/{image}'
            all_actions_dictionary[sub_directory][image.split('.')[0]] = get_sprites(current_image_path, 4, 32, 34, 3)
            
    return all_actions_dictionary