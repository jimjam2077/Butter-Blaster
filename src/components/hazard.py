import math
import random
import pygame as pg
from config import Config
from components.bullet import Bullet
from utils.asset_loader import AssetLoader

class Hazard(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetLoader.load_hazard()
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(Config.WIDTH, Config.WIDTH+300), random.randint(40, Config.HEIGHT-40))
        self.speed = -200

    def update(self, delta_time):
        self.rect.move_ip(self.speed*delta_time, 0)
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)