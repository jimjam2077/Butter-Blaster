import pygame as pg
from utils.asset_loader import AssetLoader


class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = AssetLoader.load_explosion()
        self.image_index = 0
        self.frame_duration = 1 / len(self.images)  # animation should take 1 second
        self.time_since_last_frame = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=center)
        self.speed = -200

    def update(self, dt):
        self.rect.move_ip(self.speed * dt, 0)
        self.time_since_last_frame += dt
        if self.image_index < len(self.images) - 1:
            if self.time_since_last_frame >= self.frame_duration:
                self.image_index += 1
                self.image = self.images[self.image_index]
                self.time_since_last_frame = 0
        else:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)