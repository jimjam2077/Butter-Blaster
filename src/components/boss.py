import math
import random
import pygame as pg
from config import Config
from components.bullet import Bullet
from components.explosion import Explosion
from utils.asset_loader import AssetLoader


class Boss(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetLoader.load_boss_img()
        self.rect = self.image.get_rect(right= Config.WIDTH-30, centery =Config.HEIGHT/2)
        self.mask = pg.mask.from_surface(self.image)
        
        # boss stats
        self.current_health = 0
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 150
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 0.75 * self.max_health / 100
        self.shot_delay = Config.SHOT_DELAY
        self.portrait = AssetLoader.load_avatar("andy")
        self.portrait = pg.transform.scale(self.portrait, (30, 30))
        self.port_rect = self.portrait.get_rect(topleft = (Config.WIDTH/2 + self.health_bar_length+20,10))
        
        #used for animations
        self.speed = 200
        self.moves = {
            "idle": [AssetLoader.load_boss_img()],
            "mouth": AssetLoader.load_sprite_list("boss/mouth"),
            "eye": AssetLoader.load_sprite_list("boss/eye"),
            "spider": AssetLoader.load_sprite_list("boss/spider")
            }
        self.current_move = "idle"
        self.state = "idle"
        self.current_frame = 0
        self.num_frames = len(self.moves[self.current_move])
        self.animation_speed = 0.5  # 2 frames per second
        self.animation_timer = 0.0
        
        # ability lengths and cooldowns
        self.spider_time = 3
        self.suck_time = 5      
        self._last_shot_time = 0 #used to limit fire rate later

    def update_animation(self, dt):
        frames = self.moves[self.current_move]
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame >= self.num_frames:
                self.current_frame = 0
                self.state = "idle"
            self.image = frames[self.current_frame]
            self.animation_timer -= self.animation_speed

    def perform_action(self):
        if self.state == "idle":
            self.current_move = random.choice(["mouth", "eye", "spider"])
            self.num_frames = len(self.moves[self.current_move])
            self.current_frame = 0
            self.state = "attacking"

    
    def update(self, sprite_handler, dt):
        if self.state == "attacking":
            self.update_animation(dt)
        else:
            self.perform_action()
    
    def add_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0
   
   
    def beam_attack(self):
        pass
    
    def laser_attack(self):
        pass
    
    def suck_attack(self):
        pass
    
    def spawn_adds(self):
        pass    
   
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
        health_bar = pg.Rect(Config.WIDTH/2+10, 10, health_bar_width, bar_height)
        transition_bar = pg.Rect(health_bar.right,10,transition_width, bar_height)
        transition_bar.normalize()
        
        screen.blit(self.portrait, self.port_rect)
        pg.draw.rect(screen,(0,255,0),health_bar, 0, 5)
        pg.draw.rect(screen,transition_color,transition_bar, 0, 5)	
        pg.draw.rect(screen,(119,119,119),(Config.WIDTH/2+10, 10, self.health_bar_length, bar_height), 2, 5)
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)