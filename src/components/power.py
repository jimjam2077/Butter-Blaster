import math
import random
import pygame as pg
from config import Config
from utils.asset_loader import AssetLoader


class Power(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image, self.name = AssetLoader.load_powerup()
        self.rect = self.image.get_rect(center=center)
        self.speed = -200

    def get_name(self):
        return self.name
    
    def update(self, sprite_handler, dt):
        self.rect.move_ip(self.speed*dt, 0)
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)


