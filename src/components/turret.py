import math
import random
import pygame as pg
from src.config import Config
from src.components.bullets.aiming_bullet import AimingBullet
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader

class Turret(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(list(AssetLoader.entities["turrets"].values()))
        positions = [
            {"rotation": 0, "y_loc": Config.HEIGHT},
            {"rotation": 180, "y_loc": 0}
        ]
        selected_position = random.choice(positions)
        
        self.image = pg.transform.rotate(self.image, selected_position["rotation"])
        anchor = "midtop" if selected_position["rotation"] == 180 else "midbottom" # need to determine by which edge to orient the sprite
        self.rect = self.image.get_rect(**{anchor: (random.randint(Config.WIDTH, Config.WIDTH + 200), selected_position["y_loc"])})
        
        self.mask = pg.mask.from_surface(self.image)
        self.speed = -200
        self._last_shot_time = 0
        self._shot_delay = random.uniform(2,5)
        

    def shoot(self, sprite_handler):
        turret_x = self.rect.centerx
        turret_y = self.rect.centery
        target_x_values = [-720, 0, 310]
        target_y = 0 if (turret_y > Config.HEIGHT/2) else Config.HEIGHT
        for target_x in target_x_values:
            target_pos = (turret_x + target_x, target_y)
            bullet = AimingBullet(self.rect.center, 300, "turret_bullets", random.choice(list(AssetLoader.bullets["turret_bullets"].keys())), target_pos, rotate=True)
            sprite_handler.add_enemy_bullet(bullet)
        self._last_shot_time = 0  # Reset the shot time


    def update(self, sprite_handler, dt):
        self.rect.move_ip(self.speed*dt, 0)
        self._last_shot_time += dt
        if self._last_shot_time >= self._shot_delay:
            self.shoot(sprite_handler)
        if self.rect.right < 0: # killed if offscreen
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
