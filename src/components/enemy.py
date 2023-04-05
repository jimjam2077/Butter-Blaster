
import math
import random
import pygame as pg
from config import Config


class Enemy(pg.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pg.image.load("assets/enemydorito.png")
        self.rect = self.image.get_rect()
        self.rect.center=(Config.WIDTH, random.randint(40, Config.HEIGHT-40)) 
        self.angle = 0
        self.original_image = self.image.copy()
 
      def update(self):
                  # rotate the image based on the angle
        #self.image = pg.transform.rotate(self.original_image, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)            
        self.angle += 0.4  # increment angle
        x = -10  # horizontal speed (negative for moving left)
        y = 5 * math.sin(self.angle) # vertical displacement
        self.rect.move_ip(x, y)
        if (self.rect.right < 0): # check if object goes beyond the left edge
            self.rect.right = Config.WIDTH
            self.rect.centery = random.randint(40, Config.HEIGHT - 40)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 