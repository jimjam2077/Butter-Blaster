import pygame as pg
from utils.asset_loader import AssetLoader


class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = AssetLoader.load_explosion()
        self.image_index = 0
        self.animation_speed = 3
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=center)
        self.speed = -5

    def update(self, clock):
        self.rect.move_ip(self.speed, 0)
        if self.image_index < len(self.images) - 1:
            # Change the image every `animation_speed` frames
            if clock.get_rawtime() % self.animation_speed == 0:
                self.image_index += 1
                self.image = self.images[self.image_index]
        else:
            # If the last image is displayed, kill the sprite
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)