import random
import pygame as pg
from src.utils.asset_loader import AssetLoader

class Background():
    def __init__(self):
        self.img_one = random.choice(list(AssetLoader.backgrounds["level"].values()))
        self.img_two = random.choice(list(AssetLoader.backgrounds["level"].values()))
        self.rect = self.img_one.get_rect()
        self.alt_img_one = random.choice(list(AssetLoader.backgrounds["boss"].values()))
        self.alt_img_one.set_alpha(0)
    
        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rect.width

        self.moving_speed = 100
            
    def update(self, sprite_handler, dt):
        self.bgX1 -= self.moving_speed * dt
        self.bgX2 -= self.moving_speed * dt
        if self.bgX1 <= -self.rect.width:
            self.bgX1 = self.rect.width
            self.img_one = random.choice(list(AssetLoader.backgrounds["level"].values()))
        if self.bgX2 <= -self.rect.width:
            self.bgX2 = self.rect.width
            self.img_two = random.choice(list(AssetLoader.backgrounds["level"].values()))
            
    def change_speed(self, new_speed):
        self.speed = new_speed
            
    def fade_boss_bg(self, dt):
        # Calculate the change in alpha and speed per second
        alpha_change = 255 / 2  # Reduce alpha by 255 in 1 second
        speed_change = 100 / 2  # Reduce speed by 100 units in 1 second
        # Reduce alpha of img_one and img_two if they are greater than 0
        if self.alt_img_one.get_alpha() < 255:
            self.alt_img_one.set_alpha(min(255, self.alt_img_one.get_alpha() + int(alpha_change * dt)))
        # Reduce speed gradually
        self.moving_speed = max(0, self.moving_speed - speed_change * dt)

             
    def draw(self, screen):
        screen.blit(self.img_one, (self.bgX1, self.bgY1))
        screen.blit(self.img_two, (self.bgX2, self.bgY2))
        screen.blit(self.alt_img_one, (0, 0))
