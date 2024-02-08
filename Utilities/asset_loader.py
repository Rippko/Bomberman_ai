import pygame

class AssetLoader(object):
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AssetLoader, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        self.wall_img = pygame.image.load('Assets/Wall/wall.png')
        self.crate_img = pygame.image.load('Assets/Crate/crate.png')