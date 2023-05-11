import math
import random
import pygame as pg
from config import Config
from components.boss_bullet import Bullet
from components.explosion import Explosion
from utils.asset_loader import AssetLoader


class Boss(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetLoader.load_boss_img()
        self.rect = self.image.get_rect(right= Config.WIDTH-30, centery =Config.HEIGHT/2)
        self.mask = pg.mask.from_surface(self.image)
        self.beard_rect = self.rect.copy()  # make a copy of self.rect
        self.beard_rect.height //= 4  # reduce the height to one third of the original
        self.beard_rect.bottom = self.rect.bottom-100  # set the bottom of the new rect to the bottom of self.rect
        self.beard_rect.width //= 1.5
        self.beard_rect.centerx = self.rect.centerx
        self.mouth_rect = self.beard_rect.copy()
        self.mouth_rect.height //= 2
        self.mouth_rect.width //= 4
        self.mouth_rect.left = self.beard_rect.left+50
        self.mouth_rect.top = self.beard_rect.top+10

        
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
        self.frames = []
        self.current_frame = 0
        self.num_frames = len(self.moves[self.current_move])
        self.animation_speed = 0.25  # 2 frames per second
        self.animation_timer = 0.0
        
        # ability lengths and cooldowns
        self.swarm_size = 3
        self.start_time = 0
        self.suck_time = 5000      
        self._last_shot_time = 0 #used to limit fire rate later
        self._attack_delay = 0


    def update_animation(self, dt):
        self.frames = self.moves[self.current_move]
        self.animation_timer += dt
        now = pg.time.get_ticks()   
        if self.current_frame < self.num_frames:
            self.image = self.frames[self.current_frame]
            if self.animation_timer >= self.animation_speed:
                self.current_frame += 1
                self.animation_timer = 0
                self.start_time = now
        elif self.current_move == "mouth":
            if now - self.start_time <= self.suck_time:
                self.image = self.frames[self.num_frames-1]
            else:
                self.current_frame = self.num_frames-1
                self.image = self.frames[self.current_frame]
                self.state = "aftercast"
        else:
            self.current_frame = self.num_frames-1
            self.image = self.frames[self.current_frame]
            self.state = "aftercast"


    def become_idle(self, dt):
        self.frames = self.moves[self.current_move]
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame -= 1
            if self.current_frame < 0:
                self.current_frame = 0
                self.image = self.moves["idle"][0]
                self.state = "idle"
            else:
                self.image = self.frames[self.current_frame]
            self.animation_timer = 0
        else:
            self.image = self.frames[self.current_frame]


    def choose_action(self):
            self.current_move = random.choice(["mouth", "eye", "spider"])
            self.num_frames = len(self.moves[self.current_move])
            self.current_frame = 0
            self.state = "attacking"

    
    def update(self, sprite_handler, dt):
        if self.state == "attacking":
            self.update_animation(dt)
        elif self.state == "aftercast":
            self.become_idle(dt)
        else:
            self.choose_action()    
            
        # Call the appropriate behavior method based on the sprite's current attack
        if self.current_move == "mouth":
            self.suck_attack(sprite_handler)
        elif self.current_move == "eye" and self.current_frame == self.num_frames-1:
            self.laser_attack()
        elif self.current_move == "spider" and self.state == "attacking":
            self.beam_attack(sprite_handler)
    
    
    
    def add_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0
   
   
    def beam_attack(self, sprite_handler):
        self._attack_delay = 75
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self._attack_delay:
            for x in range (0,self.swarm_size):
                rand_x = random.randint(self.beard_rect.left, self.beard_rect.right)
                rand_y = random.randint(self.beard_rect.top, self.beard_rect.bottom)
                bullet = Bullet((rand_x, rand_y), "spider.png", 500, sprite_handler.player.rect.center)
                sprite_handler.add_enemy_bullet(bullet)
                self._last_shot_time = now 
    
    def laser_attack(self):
        pass
    
    def suck_attack(self, sprite_handler):
        self._attack_delay = 200
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self._attack_delay:
            # randomly choose a side (top, left, or bottom)
            side = random.choice(['top', 'left', 'bottom'])
            if side == 'top':
                # generate a point outside the top side
                rand_x = random.randint(-20, Config.WIDTH)
                rand_y = -20
            elif side == 'left':
                # generate a point outside the left side
                rand_x = -20
                rand_y = random.randint(-20, Config.HEIGHT)
            else:  # bottom
                # generate a point outside the bottom side
                rand_x = random.randint(-20, Config.WIDTH)
                rand_y = Config.HEIGHT + 20
            bullet = Bullet((rand_x, rand_y), "dorito.png", 300, self.mouth_rect.center)
            sprite_handler.add_enemy_bullet(bullet)
            self._last_shot_time = now 
    
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
        #debug rects
        # assuming you have created the beard_rect as described
        pg.draw.rect(screen, (255, 255, 255), self.beard_rect, 3)
        pg.draw.rect(screen, (255, 0, 0), self.mouth_rect, 3)
        
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # assuming you have created the beard_rect as described
        pg.draw.rect(screen, (255, 0, 0), self.beard_rect)