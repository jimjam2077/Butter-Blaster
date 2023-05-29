import math
import random
import pygame as pg
from src.config import Config
from src.utils.asset_loader import AssetLoader


class Power(pg.sprite.Sprite):
    def __init__(self, center, speed=200):
        super().__init__()
        self.image, self.name = AssetLoader.get_random_power()
        self.rect = self.image.get_rect(center=center)
        self.speed = speed

    def get_name(self):
        return self.name
    
    def update(self, sprite_handler, dt):
        self.rect.move_ip(-self.speed*dt, 0)
        if self.rect.right < 0: # kills a power as it moves off the screen
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)


