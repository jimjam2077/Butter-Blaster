import math
import random
import pygame as pg
from config import Config


class Enemy(pg.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pg.image.load("assets/sprites/enemy"+str(random.randint(1,4))+".png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(Config.WIDTH, Config.WIDTH+400), random.randint(40, Config.HEIGHT-40))
        self.angle = 0
  
 
      def update(self, enemies):
                  # rotate the image based on the angle
        #self.image = pg.transform.rotate(self.original_image, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)            
        # add some randomness to the horizontal and vertical speed
        x = random.uniform(-10, -8)  # horizontal speed (negative for moving left)
        y = random.uniform(-1, 1)   # vertical speed
      
        # add some variability to the angle of movement
        self.angle += random.uniform(-0.05, 0.05)  # increment angle
      
        # update the position based on the speed and angle
        dx = x + math.sin(self.angle) * random.uniform(0, 1.2) # horizontal displacement
        dy = y + math.cos(self.angle) * random.uniform(0, 1.2) # vertical displacement
        self.rect.move_ip(dx, dy)
        if (self.rect.right < 0): # check if object goes beyond the left edge
            self.rect.centerx = random.randint(Config.WIDTH, Config.WIDTH+500)
            self.rect.centery = random.randint(40, Config.HEIGHT - 40)
        
        # check for collisions with other enemies
        for enemy in enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                if self.rect.centerx < enemy.rect.centerx:
                    enemy.rect.left+=1
                    self.rect.right-=1
                else:
                    enemy.rect.right-=1
                    self.rect.left+=1
 
 
      def draw(self, screen):
        screen.blit(self.image, self.rect)
        
