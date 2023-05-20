import math
import random
import pygame as pg
from config import Config
from components.explosion import Explosion
from components.bullets.aiming_bullet import AimingBullet
from components.bullets.straight_bullet import StraightBullet
from components.enemy import Enemy
from utils.audio_loader import AudioLoader
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
        #UI stuff
        self.font = AssetLoader.load_story_font(24)
        self.warning_text = self.font.render("Andy is hunkerin' down...", True, (255, 255, 255))
        self.warning_rect = self.warning_text.get_rect(midbottom = (Config.WIDTH/2, Config.HEIGHT-10))
        """         # Create a new surface with a border and background
        border_width = 2  # Adjust the border width as needed
        new_width = self.warning_rect.width + border_width * 2
        new_height = self.warning_rect.height + border_width * 2
        new_surface = pg.Surface((new_width, new_height))
        new_surface.fill((0,0,0))
        # Draw the border on the new surface
        pg.draw.rect(new_surface, (255,255,255), new_surface.get_rect(), border_width)
        # Blit the text surface onto the new surface with an offset to create the border effect
        new_surface.blit(self.warning_text, (border_width, border_width))
        # Set the updated text surface and its rect as the score_text and score_rect variables
        self.warning_text = new_surface
        self.warning_rect = new_surface.get_rect(midbottom=(Config.WIDTH / 2, Config.HEIGHT - 10)) """
        
        
        # boss stats
        self.current_health = 0
        self.target_health = 1500
        self.max_health = 1500
        self.health_bar_length = 150
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 0.75 * self.max_health / 100
        self.shot_delay = Config.SHOT_DELAY
        self.portrait = AssetLoader.load_avatar("andy")
        self.portrait = pg.transform.scale(self.portrait, (30, 30))
        self.port_rect = self.portrait.get_rect(topleft = (Config.WIDTH/2 + self.health_bar_length+20+46,10))
        
        #used for animations
        self.speed = 200
        self.moves = {
            "idle": {"frames": [AssetLoader.load_boss_img()], "duration": 0, "cooldown": 0},
            "mouth": {"frames": AssetLoader.load_sprite_list("boss/mouth"), "duration": 6, "cooldown": 2},
            "eye": {"frames": AssetLoader.load_sprite_list("boss/eye"), "duration": 7,"cooldown": 5},
            "spider": {"frames": AssetLoader.load_sprite_list("boss/spider"), "duration": 0,"cooldown": 1}
        }
        self.current_move = "idle"
        self.state = "idle"
        self.frames = []
        self.current_frame = 0
        self.num_frames = len(self.moves[self.current_move]["frames"])
        self.animation_speed = 0.25  # 2 frames per second
        self.animation_timer = 0.0
        self.destination = None
        self.speed = 100
        
        # ability lengths and cooldowns
        self.swarm_size = 3
        self.start_time = 0 
        self._last_shot_time = 0 #used to limit fire rate later
        self._attack_delay = 0
        self.hunker_time = 6
        self.hunkering = False
        
        # Starting points and directions for a patterned attack
        self.grid_starts = [
            ((Config.WIDTH-300, 0), (-1, 0)), # Spawn from right to left on top
            ((Config.WIDTH-300, 150), (0, 1)), # Spawn from top to bottom on right
            ((0, Config.HEIGHT), (1, 0)), # Spawn from left to right on bottom
        ]
        random.shuffle(self.grid_starts) # randomise the order
        self.grid_index = 0
        self.grid_blt_width = 100
        self.grid_spacing = 100
        self.grid_delay = 0
        self.current_bullet = 0
        self.bullet_count = 0

    
    def alive(self):
        """ Checks if this player object's target health is below 0.
            This happens when the player takes damage and the healthbar is updating.

        Returns:
            int: The target health of the player, based on the current damage calculation.
        """
        return self.target_health > 0
        
    def update_animation(self, dt):
        self.frames = self.moves[self.current_move]["frames"]
        self.animation_timer += dt

        if self.current_frame < self.num_frames: # not on the last frame
            self.image = self.frames[self.current_frame] # set the image
            if self.animation_timer >= self.animation_speed: # time to update the current frame
                self.current_frame = min(self.current_frame + 1, self.num_frames-1)
                self.animation_timer = 0 #reset the animation timer
                if self.current_frame < self.num_frames-1: # not on the last frame
                    self.start_time = 0
        if self.current_frame == self.num_frames-1 and self.state != "aftercast":
            if "duration" in self.moves[self.current_move]:
                #print(self.start_time)
                self.start_time += dt
                if self.start_time >= self.moves[self.current_move]["duration"]:
                    self.state = "aftercast"
                    self.animation_timer = 0


    def become_idle(self, dt):
        self.frames = self.moves[self.current_move]["frames"] # get the frames for the current move
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame = max(self.current_frame-1, 0)
            self.image = self.frames[self.current_frame]
            if self.current_frame == 0:
                self.state = "idle"
                self.image = self.moves["idle"]["frames"][0]
                random.shuffle(self.grid_starts)
                self.grid_index = 0
            self.animation_timer = 0
        else:
            self.image = self.frames[self.current_frame]



    def choose_action(self):
            self.current_move = random.choice(["mouth", "eye", "spider"])
            self.num_frames = len(self.moves[self.current_move]["frames"])
            self.current_frame = 0
            self.start_time = 0
            self.state = "attacking"
            AudioLoader.attack_sound(self.current_move)

    
    def update(self, sprite_handler, dt):
        self.hunker(sprite_handler, dt)
        if self.hunkering:
            return  # Skip the rest of the functionality if hunkering is true
        if not self.current_move == "mouth": #don't move during mouth
            top = self.rect.y
            bottom = self.rect.y + self.rect.height
            if self.destination is None or top <= 20 or bottom >= Config.HEIGHT - 20 or (top <= self.destination <= bottom):
                self.destination = self.select_destination()

            if bottom < self.destination:
                self.rect.move_ip(0, self.speed*dt)
                self.beard_rect.move_ip(0, self.speed*dt)
                self.mouth_rect.move_ip(0, self.speed*dt)
            elif top >self.destination:
                self.rect.move_ip(0, -self.speed*dt)
                self.beard_rect.move_ip(0, -self.speed*dt)
                self.mouth_rect.move_ip(0, -self.speed*dt)
    
        
        if self.state == "attacking":
            self.update_animation(dt)
        elif self.state == "aftercast":
            self.become_idle(dt)
        else:
            self.choose_action()    
            
        # Call the appropriate behavior method based on the sprite's current attack
        if self.current_move == "mouth" and self.start_time < self.moves["mouth"]["duration"]/1.5:
            self.suck_attack(sprite_handler, dt)
        elif self.current_move == "eye" and self.state == "attacking":
            self.grid_attack(sprite_handler, dt)
        elif self.current_move == "spider" and self.state == "attacking":
            self.swarm_attack(sprite_handler, dt)
        

    
    
    def add_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0
   
   
    def swarm_attack(self, sprite_handler, dt):
        self._attack_delay = 0.025 # time in seconds
        self._last_shot_time +=dt
        if self._last_shot_time >= self._attack_delay:
            for x in range (0,self.swarm_size):
                rand_x = random.randint(self.beard_rect.left, self.beard_rect.right)
                rand_y = random.randint(self.beard_rect.top, self.beard_rect.bottom)
                bullet = AimingBullet((rand_x, rand_y), 700, "spider.png", sprite_handler.player.rect.center)
                sprite_handler.add_enemy_bullet(bullet)
                self._last_shot_time = 0
    
    
    def grid_attack(self, sprite_handler, dt):
        self._attack_delay = 0.15 # time in seconds
        self._last_shot_time += dt
        if self._last_shot_time < self._attack_delay:
            return
        self._last_shot_time = 0
        if self.grid_index < 3:
            start_point, spawn_direction = self.grid_starts[self.grid_index] # get the current statistics
            bullet_dir = self.inward_direction(spawn_direction) # set the flight direction perpendicular to spawn dir
            if self.bullet_count == 0: # set how many bullets can fit in the current direction
                self.bullet_count = (Config.WIDTH if spawn_direction[0] != 0 else Config.HEIGHT) // (self.grid_blt_width + self.grid_spacing)
            elif self.current_bullet < self.bullet_count:
                x = start_point[0] + self.current_bullet * (self.grid_blt_width + self.grid_spacing) * spawn_direction[0]
                y = start_point[1] + self.current_bullet * (self.grid_blt_width + self.grid_spacing) * spawn_direction[1]
                bullet = StraightBullet((x,y), 650, f"baby{random.randint(1,10)}.png", bullet_dir[0], bullet_dir[1], True, self.grid_delay)
                sprite_handler.add_enemy_bullet(bullet)
                self.grid_delay += 0.25
                self.current_bullet += 1
            else:
                self.grid_index += 1
                self.current_bullet = 0
                self.bullet_count = 0
        else:
            self.grid_delay = 0
            random.shuffle(self.grid_starts)

        
    
    def suck_attack(self, sprite_handler, dt):
        self._attack_delay = 0.225 # time in seconds
        self._last_shot_time += dt
        if self._last_shot_time >= self._attack_delay:
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
            bullet = AimingBullet((rand_x, rand_y), 500, "dorito.png", self.mouth_rect.center)
            sprite_handler.add_enemy_bullet(bullet)
            self._last_shot_time = 0
    
    def spawn_adds(self):
        pass    
   
    def inward_direction(self, direction):
        x, y = direction
        if x == 0 and y == -1:
            return (1, 0)
        return (-y, -x)

    def select_destination(self):
        destination = random.randint(20, 700)
        print(destination)
        return destination

    def hunker(self, sprite_handler, dt):
        if random.random() < 0.10 and self.state == "idle":  # 1% chance to set hunkering to true
            self.hunkering = True
        if self.hunkering:
            self._attack_delay = 1 # time in seconds
            self._last_shot_time +=dt
            self.hunker_time -= dt
            if self._last_shot_time >= self._attack_delay:
                for x in range(1,3):
                    enemy = Enemy()
                    sprite_handler.add_enemy(enemy)
                self._last_shot_time = 0   
            if self.hunker_time <= 0:
                self.hunker_time = 6
                self.hunkering = False


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
        health_bar = pg.Rect(Config.WIDTH/2+10+47, 10, health_bar_width, bar_height)
        transition_bar = pg.Rect(health_bar.right,10,transition_width, bar_height)
        transition_bar.normalize()
        
        screen.blit(self.portrait, self.port_rect)
        if self.hunkering:
            screen.blit(self.warning_text, self.warning_rect)
        pg.draw.rect(screen,(0,255,0),health_bar, 0, 5)
        pg.draw.rect(screen,transition_color,transition_bar, 0, 5)	
        pg.draw.rect(screen,(119,119,119),(Config.WIDTH/2+10+47, 10, self.health_bar_length, bar_height), 2, 5)
        #debug rects
        # assuming you have created the beard_rect as described
        pg.draw.rect(screen, (255, 255, 255), self.beard_rect, 3)
        pg.draw.rect(screen, (255, 0, 0), self.mouth_rect, 3)
        pg.draw.rect(screen, (0, 255, 0), self.rect, 3)
        
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)