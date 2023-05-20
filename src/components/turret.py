import math
import random
import pygame as pg
from config import Config
from utils.asset_loader import AssetLoader

class Turret(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetLoader.load_turret()
        positions = [
            {"rotation": 0, "y_loc": Config.HEIGHT},
            {"rotation": 180, "y_loc": 0}
        ]
        selected_position = random.choice(positions)
        self.image = pg.transform.rotate(self.image, selected_position["rotation"])
        self.rect = self.image.get_rect(midbottom = (random.randint(Config.WIDTH, Config.WIDTH + 200), selected_position["y_loc"]))
        self.mask = pg.mask.from_surface(self.image)
        self.speed = -200

    def update(self, sprite_handler, dt):
        self.rect.move_ip(self.speed*dt, 0)
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
