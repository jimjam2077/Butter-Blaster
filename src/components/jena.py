import math
import random
import pygame as pg
from src.config import Config
from src.components.bullets.straight_bullet import StraightBullet
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader

class Jena(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # loading the ship
        self.image = AssetLoader.entities["npcs"]["jena"]
        self.mask = pg.mask.from_surface(self.image)  # create a mask from the sprite's image
        self.rect = self.mask.get_rect()  # set the rect to match the mask
        
        self.portrait = AssetLoader.ui_parts["portraits"]["jena"]
        self.portrait = pg.transform.scale(self.portrait, (40, 40))
        self.port_rect = self.portrait.get_rect(center = (Config.WIDTH/2, Config.HEIGHT/2))
        self.font = AssetLoader.fonts["ui"]
        self.text = self.font.render("Meow!", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(midleft = (self.port_rect.right + 10, self.port_rect.centery))
        # set up movement statistics
        self.speed = 230
        self.pos = [random.randint(-Config.WIDTH/2, Config.WIDTH/2), -self.rect.height] #initial spawn point
        self.angle = 0
        self._last_shot_time = 0 
        self._shot_delay = 100 # decrease to fire quicker
        AssetLoader.sfx["meow"].play()
        
        
    def shoot(self, sprite_handler):
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self._shot_delay:
            if self.rect.centerx > Config.WIDTH or self.rect.centery < 0:
                return
            bullet = StraightBullet((self.rect.right, self.rect.centery), Config.BULLET_SPEED, "bullets", "ally", 1, 0)
            sprite_handler.add_bullet(bullet)
            AssetLoader.sfx["shoot"].play()
            self._last_shot_time = now 

    def update(self, sprite_handler, dt):
        # Update the position of the Jena sprite
        x = self.pos[0] + self.speed * dt * math.sin(math.radians(self.angle))
        y = self.pos[1] + self.speed * dt * math.cos(math.radians(self.angle))
        self.pos = [x, y]
        self.rect.center = tuple(self.pos)
        self.angle += 1  # Rotate at 1 degree per frame
        if self.angle > 360 or self.rect.centerx >= Config.WIDTH+20 or self.rect.centery < -100:
            sprite_handler.remove_assist()
            
        # add a portrait + "meow!" at bottom center, small
        self.shoot(sprite_handler)
    


    def draw(self, screen):
        # Rotate the Jena sprite
        #rotated_image = pg.transform.rotate(self.image, -self.angle)
        #rotated_rect = rotated_image.get_rect(center=self.rect.center)
        #screen.blit(rotated_image, rotated_rect)
        # Draw the Jena sprite
        screen.blit(self.image, self.rect)
        screen.blit(self.portrait, self.port_rect)
        screen.blit(self.text, self.text_rect)