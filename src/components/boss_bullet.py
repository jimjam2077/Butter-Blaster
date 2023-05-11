import pygame
from config import Config

from utils.asset_loader import AssetLoader

import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, img_name, speed, target_pos=None):
        super().__init__()
        self.type = img_name
        self.image = AssetLoader.load_bullet(img_name)
        self.rect = self.image.get_rect(center=pos)  # set the initial position of the bullet
        self.target_pos = target_pos  # store the target position
        self.speed = speed  # set the speed of the bullet
        self.rotated_image = self.image  # initialize rotated image to be the same as original image
        self.mask = pygame.mask.from_surface(self.image)  # create collision mask from bullet's image

        if self.target_pos is not None:
            # calculate angle between bullet's current position and target position
            dx = self.target_pos[0] - self.rect.x
            dy = self.target_pos[1] - self.rect.y
            angle = math.degrees(math.atan2(-dy, dx))
            # rotate the bullet's image by the angle
            self.rotated_image = pygame.transform.rotate(self.image, angle)
            # update the rect of the bullet's rotated image
            self.rect = self.rotated_image.get_rect(center=pos)
            # update the collision mask of the rotated image
            self.mask = pygame.mask.from_surface(self.rotated_image)
            self.direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(self.rect.center)
            self.direction.normalize_ip()
            # calculate the original distance between the bullet's starting position and its target position




    def update(self, sprite_handler, dt):
        if self.target_pos is not None:   
            # move the bullet in a straight line
            self.rect.move_ip(self.direction * self.speed * dt)
            
            # check if the bullet has moved off the screen
            if self.rect.right < 0:
                # remove the bullet from the sprite group
               self.kill
        else:
            #simply move left on x axis
            pass
       


        if "dorito" in self.type:
            if self.rect.colliderect(pygame.Rect(self.target_pos[0]-10, self.target_pos[1]-10, 20, 20)) or self.rect.left > self.target_pos[0]:
                self.kill()

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.rotated_image, self.rect)
