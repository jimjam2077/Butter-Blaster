import pygame as pg
from config import Config

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("assets/sprites/bullets/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery =y
        
    def update(self):
        self.rect.move_ip(Config.BULLET_SPEED, 0)
        if self.rect.right >= Config.WIDTH:
            self.kill()
            
    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)