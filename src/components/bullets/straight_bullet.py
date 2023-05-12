import pygame
from components.bullets.bullet import Bullet
from config import Config


# represents a bullet which can only travel in a straight line in one direction
class StraightBullet(Bullet, pygame.sprite.Sprite):
    def __init__(self, pos, speed, img_name, x_dir, y_dir, rotate=False):
        super().__init__(pos, speed, img_name)
        self.x_dir = x_dir
        self.y_dir = y_dir
        if x_dir == 1 and y_dir == 0:
            self.angle = 180
        elif x_dir == -1 and y_dir == 0:
            self.angle = 0
        elif x_dir == 0 and y_dir == 1:
            self.angle = 90
        elif x_dir == 0 and y_dir == -1:
            self.angle = 270
        else:
            raise ValueError("Invalid x_dir and y_dir values.")
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.rotate = rotate

        
    def update(self, sprite_handler, dt):
            if self.rotate == True:
                self.angle = (self.angle + 1) % 360
                self.image = pygame.transform.rotate(self.rotated_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.move_ip(self.x_dir * (self.speed *dt), self.y_dir * (self.speed *dt))
            # Check if bullet has moved off the screen
            if self.rect.right < 0 or self.rect.left > Config.WIDTH or self.rect.bottom < 0 or self.rect.top > Config.HEIGHT:
                self.kill()
                
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)