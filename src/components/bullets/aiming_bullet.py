import pygame
from config import Config
from components.bullets.bullet import Bullet
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
import math

# represents a bullet which can only travel in a straight line in one direction
class AimingBullet(Bullet, pygame.sprite.Sprite):
    def __init__(self, pos, speed, img_name, target_pos, rotate=False, delay = 0):
        super().__init__(pos, speed, img_name, delay)
        self.type = img_name
        self.target_pos = target_pos  # store the target position
        dx = self.target_pos[0] - self.rect.centerx # x distance
        dy = self.target_pos[1] - self.rect.centery # y distance
        angle = math.degrees(math.atan2(-dy, dx))
        # rotate the bullet's image by the angle
        self.rotated_image = pygame.transform.rotate(self.image, angle)
        # set the center of rotation to the center of the original image
        rect = self.rotated_image.get_rect(center=self.rect.center)
        self.rect = rect
        self.image = self.rotated_image
        self.mask = pygame.mask.from_surface(self.image)
        #direction to face
        self.direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(self.rect.center)
        self.direction.normalize_ip()
        self.rotate = rotate
        self.angle = 0

        
    def update(self, sprite_handler, dt):
        if self.rotate == True:
            self.angle = (self.angle + 5) % 360
            self.image = pygame.transform.rotate(self.rotated_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.move_ip(self.direction * self.speed * dt)
        if self.rect.right < 0:
            self.kill()       
        elif "dorito" in self.type:
            if self.rect.colliderect(pygame.Rect(self.target_pos[0]-15, self.target_pos[1]-15, 30, 30)) or self.rect.left > self.target_pos[0]:
                AudioLoader.crunch_sound()
                self.kill()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)