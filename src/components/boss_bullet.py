import pygame
from config import Config
from utils.asset_loader import AssetLoader
import math


#TODO: I don't know why, but I can't seem to get the image to rotate correctly.
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
        #self.angle = 0

        if self.target_pos is not None:
            # calculate angle between bullet's current position and target position
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            angle = math.degrees(math.atan2(-dy, dx))
            # rotate the bullet's image by the angle
            rotated_image = pygame.transform.rotate(self.image, angle)
            # set the center of rotation to the center of the original image
            rect = rotated_image.get_rect(center=self.rect.center)
            self.rect = rect
            self.rotated_image = rotated_image
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
               self.kill()
        else:
            #simply move left on x axis
            pass
       

        if "dorito" in self.type:
            if self.rect.colliderect(pygame.Rect(self.target_pos[0]-15, self.target_pos[1]-15, 30, 30)) or self.rect.left > self.target_pos[0]:
                self.kill()


    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)
