import pygame
from config import Config
from utils.asset_loader import AssetLoader
import math


# base bullet class to inherit from
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, img_name, delay = 0):
        super().__init__()
        self.image = AssetLoader.load_bullet(img_name)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.delay = delay
        
    def update(self, sprite_handler, dt):
        pass
            
    def draw(self, screen):
        pass