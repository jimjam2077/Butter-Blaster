import pygame
from src.config import Config
from src.utils.asset_loader import AssetLoader
import math


# base bullet class to inherit from
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, type, name, delay = 0):
        super().__init__()
        self.image = AssetLoader.bullets[type][name]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.delay = delay 
    
    def kill_out_of_bounds(self): #ensures that bullets are killed if they move off-screen
        if self.rect.centerx < -50 or self.rect.centerx > Config.WIDTH+50 or self.rect.centery < -50 or self.rect.centery > Config.HEIGHT+50:
            self.kill()
    
    def update(self, sprite_handler, dt):
        pass
            
    def draw(self, screen):
        pass