import math
import random
import pygame as pg
from config import Config
from components.bullet import Bullet
from utils.asset_loader import AssetLoader


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetLoader.load_enemy_ship()
        #add code here to randomise scaling
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(Config.WIDTH, Config.WIDTH+700), random.randint(40, Config.HEIGHT-40))
        self.angle = 0
        self._last_shot_time = 0 #used to limit fire rate later
        self._shot_delay = random.randint(Config.SHOT_DELAY*6, Config.SHOT_DELAY*10)
        
    def shoot(self, all_sprites, bullets):
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self._shot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.centery, True)
            bullets.add(bullet)
            all_sprites.add(bullet)
            self._last_shot_time = now
  
 
    def update(self, all_sprites, enemies, bullets):
                  # rotate the image based on the angle
        #self.image = pg.transform.rotate(self.original_image, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)            
        # add some randomness to the horizontal and vertical speed
        x = random.uniform(-5, -8)  # horizontal speed (negative for moving left)
        y = random.uniform(-2, 2)   # vertical speed - set one higher to make enemies veer up or down
      
        # add some variability to the angle of movement
        self.angle += random.uniform(-0.5, 0.5)  # increment angle
        
        
      
        # update the position based on the speed and angle
        dx = x + math.sin(self.angle) * random.uniform(0, 0) # horizontal displacement
        dy = y + math.cos(self.angle) * random.uniform(-0, 4) # vertical displacement - determines "waviness" of movement
        self.rect.move_ip(dx, dy)
        self.shoot(all_sprites, bullets)
        if (self.rect.right < 0): # check if object goes beyond the left edge
            #self.kill()
            self.rect.centerx = random.randint(Config.WIDTH, Config.WIDTH+700)
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
        
