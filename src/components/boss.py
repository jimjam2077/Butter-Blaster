import math
import random
import pygame as pg
from config import Config
from components.bullet import Bullet
from utils.asset_loader import AssetLoader


class Boss(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image, self.name = AssetLoader.load_powerup()
        self.rect = self.image.get_rect(center=center)
        self.speed = -200

    def get_name(self):
        return self.name
    
    def update(self, delta_time):
        self.rect.move_ip(self.speed*delta_time, 0)
        if self.rect.right < 0:
            self.kill()
   
    def advanced_health(self, screen):
    transition_width = 0
    transition_color = (0,255,0)
    bar_height = 15

    if self.current_health < self.target_health:
        self.current_health += self.health_change_speed
        transition_width = int((self.target_health - self.current_health) / self.health_ratio)
        transition_color = (255,255,0)

    if self.current_health > self.target_health:
        self.current_health -= self.health_change_speed 
        transition_width = int((self.target_health - self.current_health) / self.health_ratio)
        transition_color = (255,0,0)

    
    health_bar_width = int(self.current_health / self.health_ratio)
    health_bar = pg.Rect(14+self.port_rect.width,10,health_bar_width,bar_height)
    transition_bar = pg.Rect(health_bar.right,10,transition_width,bar_height)
    transition_bar.normalize()
    
    screen.blit(self.portrait, self.port_rect)
    pg.draw.rect(screen,(0,255,0),health_bar, 0, 5)
    pg.draw.rect(screen,transition_color,transition_bar, 0, 5)	
    pg.draw.rect(screen,(119,119,119),(14+self.port_rect.width,10,self.health_bar_length,bar_height),2, 5)
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)