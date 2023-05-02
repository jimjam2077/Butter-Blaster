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
        self.image = pg.transform.rotate(self.image, random.randint(0, 360))
        self.mask = pg.mask.from_surface(self.image)  # create a mask from the sprite's image
        self.rect = self.mask.get_rect()  # set the rect to match the mask
        self.rect.center=(random.randint(Config.WIDTH, Config.WIDTH+300), random.randint(40, Config.HEIGHT-40))
        self.speed = -200

    def update(self, sprite_handler, dt):
        self.rect.move_ip(self.speed*dt, 0)
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
