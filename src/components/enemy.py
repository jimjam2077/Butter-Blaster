import math
import random
import pygame as pg
from src.config import Config
from src.components.explosion import Explosion
from src.components.power import Power
from src.components.bullets.straight_bullet import StraightBullet
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(list(AssetLoader.entities["enemy_ships"].values()))
        # add code here to randomise scaling?
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(Config.WIDTH, Config.WIDTH+700), random.randint(40, Config.HEIGHT-40))
        self._last_shot_time = 0 #used to limit fire rate later
        self._shot_delay = random.randint(Config.SHOT_DELAY*3, Config.SHOT_DELAY*6)
        self.amplitude = random.randint(1,4) / abs(math.sin(0.5 * math.pi))  #wave height
        self.frequency = random.uniform(1.5, 3) #larger = tighter wave
        self.phase = random.uniform(0, math.pi*2) 
        self.time = 0  # current time
        self.x_spd = 250
        
    def shoot(self, sprite_handler):
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self._shot_delay:
            bullet = StraightBullet((self.rect.left, self.rect.centery), Config.BULLET_SPEED*0.75, "bullets", "enemy", -1, 0)
            sprite_handler.add_enemy_bullet(bullet)
            #AssetLoader.sfx["enemyshoot"].play()
            self._last_shot_time = now 
 
    def update(self, sprite_handler, dt):
        self.time += dt
        # calculate positive/negative speed according to sine calculation
        y_spd = self.amplitude * math.sin(self.frequency * self.time + self.phase)
        # update the position based on the speed and angle
        x_pos = self.x_spd *dt
        y_pos = y_spd * 60 *dt # vertical displacement - determines "waviness" of movement
        # update the rect
        self.rect.centerx -= x_pos
        self.rect.centery += y_pos
        # fire a bullet if possible
        self.shoot(sprite_handler)
        if (self.rect.right < 0): # check if object goes beyond the left edge
            # reset the position off-screen to the right
            self.rect.centerx = random.randint(Config.WIDTH, Config.WIDTH+200)
            self.rect.centery = random.randint(40, Config.HEIGHT - 40)
        
        # check for collisions with other enemies
        for enemy in sprite_handler.enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                if self.rect.centerx < enemy.rect.centerx:
                    enemy.rect.left+=1
                    self.rect.right-=1
                else:
                    enemy.rect.right-=1
                    self.rect.left+=1
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
