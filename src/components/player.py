import math
import random
import pygame as pg
from components.bullets.straight_bullet import StraightBullet
from config import Config
from components.power import Power
from components.explosion import Explosion
from components.jena import Jena
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader

vector = pg.math.Vector2
#screen margins - remember window grows down and right 0,0 is top left corner
MARGIN_TOP = 20
MARGIN_LEFT = 20
MARGIN_BOTTOM = Config.HEIGHT - 20
MARGIN_RIGHT = Config.WIDTH - 20

# passing Sprite makes Player Class a child of Sprite
# can then use super().__init__() to call the Sprite's init() function
class Player(pg.sprite.Sprite):
    _instance = None
    
        #make the class a singleton - don't want multiple player objects (for now)
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self._initialized = True
        #set up the ship image, adjust the scaling and animation speed here
        self.ammo_name = name+"bullet.png"
        self.images = AssetLoader.load_player_ship(name)
        self.image = self.images[0]
        self.mask = pg.mask.from_surface(self.image)
        self.original_image = self.image.copy()
        self.original_images = self.images.copy()
        self.animation_speed = 0.0 # adjust animation speed
        self.animation_timer = 0.032
        self.animation_frame = 0
        # set up the position and movement variables
        self.pos = vector((Config.PLAYER_POS))
        self.velocity = vector(0,0)
        self.acc = vector(0,0)
        self.rect = self.image.get_rect(center=self.pos)  # defines the borders according to image size
        # HUD elements
        self.score = 0
        self.font = AssetLoader.load_story_font(14)
        self.score_text = self.font.render(f"{self.score:03d}/200", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center = (Config.WIDTH/2, 15))
        # Print the width of the rect
        print("Width:", self.score_rect.width)
        self.health_bar_length = 150
        self.portrait = AssetLoader.load_avatar(name)
        self.ammo = pg.image.load("assets/powers/power3.png").convert_alpha()
        self.ammo_rect = self.ammo.get_rect
        self.portrait = pg.transform.scale(self.portrait, (30, 30))
        self.port_rect = self.portrait.get_rect(midright=(self.score_rect.left - (self.health_bar_length + 20), 25))
        # Damage statistics
        self._last_shot_time = 0 # used to limit fire rate later
        self.shot_delay = Config.SHOT_DELAY # determines fire rate
        self.damage = 1 # amount of damage delt by the player
        self.level = 0 # increases up to 3
        self.assists = 0 # number of times the player can summon fire support
        # Health statistics
        self.last_hit_time = 0 #used for invulnerability window
        self.current_health = 0
        self.target_health = 10
        self.max_health = 10
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 0.75 * self.max_health / 100

    def increase_score(self):
        """ Increases the player's score by 1, up to 200
        """
        self.score = min(self.score+1, 200);


    def get_score(self):
        """ Returns the current score for this player object

        Returns:
            int: the current score of the player object
        """
        return self.score


    def alive(self):
        """ Checks if this player object's target health is below 0.
            This happens when the player takes damage and the healthbar is updating.

        Returns:
            int: The target health of the player, based on the current damage calculation.
        """
        return self.target_health > 0


    def scale_image(self, factor): # not currently used, but can scale the player's image
        """Scales a player image by some factor 

        Args:
            factor (float): a float representing a percentage scaling on the image

        Returns:
            pg.Surface: a surface scaled to the new size
        """
        x_size = self.image.get_width() * factor # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * factor
        return pg.transform.scale(self.image, (x_size, y_size)) # defines a starting position for rect


    def shoot(self, sprite_handler):
        """ Creates a bullet centred on the creating entity (the player)
            and adds it to the sprite handler's bullet groups

        Args:
            sprite_handler (SpriteHandler): The SpriteHandler object responsible for managing sprites.
        """
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self.shot_delay:
            if self.level >=2: # create 2 bullets instead of 1 as the player levels up
                bullet1 = StraightBullet((self.rect.right, self.rect.centery + 8), Config.BULLET_SPEED, self.ammo_name, 1, 0)
                bullet2 = StraightBullet((self.rect.right, self.rect.centery - 8), Config.BULLET_SPEED, self.ammo_name, 1, 0)
                sprite_handler.add_bullet(bullet1)
                sprite_handler.add_bullet(bullet2)
            else: # player starts with 1 bullet    
                bullet = StraightBullet((self.rect.right, self.rect.centery), Config.BULLET_SPEED, self.ammo_name, 1, 0)
                sprite_handler.add_bullet(bullet)
            AudioLoader.attack_sound("shoot")
            self._last_shot_time = now


    def blink_ship(self):
        """ This function causes the player ship images to "blink", which indicates 
            to the player that they are currently inside the invulnerability window.
        """
        now = pg.time.get_ticks()
        blink_len = 200 # how long each blink lasts
        blink_alpha = 100 # set blink alpha value (0-255)
        # only blink the ship if it's currently invulnerable
        if now - self.last_hit_time < Config.INVULN_WINDOW:
            blink_on = (now - self.last_hit_time) % blink_len < blink_len / 2
            if blink_on:
                # create a list to store the new images
                new_images = []
                for image in self.images:
                    # create a copy of the original image and set its alpha value
                    new_image = image.copy()
                    new_image.set_alpha(blink_alpha)
                    new_images.append(new_image)
                self.images = new_images
            else:
                # revert back to the original images
                self.images = self.original_images
        else:
            # if the ship is not currently invulnerable, make sure it's fully visible
            self.images = self.original_images

  
    def handle_input(self,sprite_handler):
        """ Handles all of the key events for the player

        Args:
            sprite_handler (SpriteHandler): The sprite handler object that needs to be passed through
        """
        self.acc = vector(0,0)
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_UP] or pressed_keys[pg.K_w]:
            self.acc.y = -Config.ACC
        if pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_s]:
            self.acc.y = +Config.ACC
        if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_a]:
            self.acc.x = -Config.ACC
        if pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_d]:
            self.acc.x = +Config.ACC
        if pressed_keys[pg.K_SPACE]:
            self.shoot(sprite_handler)
        if pressed_keys[pg.K_f]:
            if self.assists > 0:
                jena = Jena()
                sprite_handler.all_sprites.add(jena)
                self.assists-=1
        #calc acceleration
        self.acc.x += self.velocity.x * Config.FRIC
        self.acc.y += self.velocity.y * Config.FRIC
        
   
    def update(self, sprite_handler, dt):
        self.handle_input(sprite_handler)
        self.score_text = self.font.render(f"{self.score:03d}/200", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center = (Config.WIDTH/2, 15))
        # limit player's movement within the screen boundaries
        if self.rect.right > MARGIN_RIGHT:
            self.velocity.x = -self.velocity.x
            self.acc.x = -self.acc.x
            self.pos.x = self.rect.width / 2
        if self.rect.left < MARGIN_LEFT:
            self.velocity.x = -self.velocity.x
            self.acc.x = -self.acc.x
            self.pos.x = self.rect.width / 2
        if self.pos.y > MARGIN_BOTTOM:
            self.velocity.x = -self.velocity.x
            self.acc.y = -self.acc.y
            self.pos.y = self.rect.height / 2
        if self.pos.y < MARGIN_TOP:
            self.velocity.x = -self.velocity.x
            self.acc.y = -self.acc.y
            self.pos.y = self.rect.height / 2
        
        #move the ship 
        self.velocity += self.acc * dt
        self.pos += self.velocity * dt
        #print("vel: " + str(self.velocity) + "acc: " + str(self.acc))
        
        # Screen boundary detection
        # offsets +/- onto the already-defined margin so the center point is correct later
        # sets x to the max of left (0) or the min of right (WIDTH) and current position
        # sets y to the max of top (0) or the min of bottom (HEIGHT) and current position
        l_x_offset = MARGIN_LEFT + self.rect.width / 2
        r_x_offset = MARGIN_RIGHT - self.rect.width / 2
        t_y_offset = MARGIN_TOP + self.rect.height / 2
        b_y_offset = MARGIN_BOTTOM - self.rect.height / 2
        self.pos.x = max(l_x_offset, min(r_x_offset, self.pos.x))
        self.pos.y = max(t_y_offset, min(b_y_offset, self.pos.y))
        # update hitbox
        self.rect.center = self.pos   
        #finally, deal with any collisions
        #self.check_enemy_hit(sprite_handler)
        #self.check_player_hit(sprite_handler)
        self.blink_ship()
        #self.check_powerup_touched(sprite_handler)
        #animate the ship
        self.animation_timer += dt
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.images)
            self.image = self.images[self.animation_frame]
            # update the original image
            self.original_image = self.image.copy() 


    def add_damage(self,amount):
        self.target_health = max(self.target_health-amount, 0)


    def add_health(self,amount):
        self.target_health = min(self.target_health+amount, self.max_health)

            
    def increase_level(self):
        self.level = min(self.level+1, 3)


    def add_assist(self):
        """ Adds 1 to the assist count to a max of 3
        """
        self.assists = min(self.assists+1, 3)
    
    def get_damage(self):
        return self.damage
    
    
    # should move this and the boss HUD code to a separate file/function
    def update_hud(self, screen):
        transition_width = 0
        transition_color = (0, 255, 0)
        bar_height = 15

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 0, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pg.Rect(self.port_rect.right + 5, 10, health_bar_width, bar_height)
        transition_bar = pg.Rect(health_bar.right, health_bar.top, transition_width, bar_height)
        transition_bar.normalize()

        screen.blit(self.portrait, self.port_rect)
        screen.blit (self.score_text, self.score_rect)
        pg.draw.rect(screen, (0, 255, 0), health_bar, 0, 5)
        pg.draw.rect(screen, transition_color, transition_bar, 0, 5)
        pg.draw.rect(screen, (119, 119, 119), (self.port_rect.right + 5, 10, self.health_bar_length, bar_height), 2, 5)
        
    
    def draw(self, screen):
         # can add other things to draw here
        screen.blit(self.images[self.animation_frame], self.rect)

        
    def reset(self):
        """ resets all of the player statistics which may have changed during gameplay
        """
        self.current_health = 1
        self.target_health = 10
        self.max_health = 10
        self.level = 0
        self.score = 0
        self.damage = 1
        self.pos = vector((Config.PLAYER_POS))
        self.shot_delay = Config.SHOT_DELAY
        


