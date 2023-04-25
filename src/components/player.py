import math
import random
import pygame as pg
from components.bullet import Bullet
from config import Config
from components.power import Power
from components.explosion import Explosion
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
        self.images = AssetLoader.load_player_ship(name)
        self.image = self.images[0]
        self.mask = pg.mask.from_surface(self.image)
        self.original_image = self.image.copy()
        self.original_images = self.images.copy()
        self.animation_speed = 30 # adjust animation speed
        self.animation_timer = 0
        self.animation_frame = 0
        # set up the position and movement variables
        self.pos = vector((Config.PLAYER_POS))
        self.velocity = vector(0,0)
        self.acc = vector(0,0)
        self.rect = self.image.get_rect(center=self.pos)  # defines the borders according to image size
        # set up the player statistics
        self.portrait = AssetLoader.load_avatar(name)
        self.portrait = pg.transform.scale(self.portrait, (30, 30))
        self.port_rect = self.portrait.get_rect(topleft = (10,10))
        self._last_shot_time = 0 #used to limit fire rate later
        self._last_hit_time = 0 #used for invulnerability window
        self.current_health = 0
        self.target_health = 5
        self.max_health = 10
        self.health_bar_length = 150
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 0.025
        self.shot_delay = Config.SHOT_DELAY
        self.level = 0


    #property getter for lives  
    def alive(self):
        return self.current_health > 0

    # not currently used for anything
    def scale_image(self, factor):
        """Scales a player image by some factor 

        Args:
            factor (float): a float representing a percentage scaling on the image

        Returns:
            pg.Surface: a surface scaled to the new size
        """
        x_size = self.image.get_width() * factor # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * factor
        return pg.transform.scale(self.image, (x_size, y_size)) # defines a starting position for rect


    def shoot(self, all_sprites, bullets):
        """Creates a bullet centred on the creating entity (the player)
        and adds it to the group

        Args:
            all_sprites (pg.Group): the sprite group containing all sprites
            bullets (_type_): the sprite group containing friendly bullets
        """
        now = pg.time.get_ticks()
        if now - self._last_shot_time > self.shot_delay:
            if self.level == 3:
                bullet1 = Bullet(self.rect.right, self.rect.centery + 8)
                bullet2 = Bullet(self.rect.right, self.rect.centery - 8)
                bullets.add(bullet1)
                bullets.add(bullet2)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
            else:     
                bullet = Bullet(self.rect.right, self.rect.centery)
                bullets.add(bullet)
                all_sprites.add(bullet)
            self._last_shot_time = now
                
    
    def check_enemy_hit(self, hazards, all_sprites, bullets, enemy_grp, powers):
        """Looks for collisions between player bullets and enemy rects
        
        Args:
            hazards (pg.Group): the sprite group containing hazards
            all_sprites (pg.Group): the sprite group containing all sprites
            bullets (pg.Group): the sprite group containing player bullets
            enemy_grp (pg.Group): the sprite group containing enemies
            powers (pg.Group): the sprite group containing powers
        """
        # Check for collisions between bullets and enemies
        bullet_enemy_collisions = pg.sprite.groupcollide(bullets, enemy_grp, True, True)

        for bullet, enemy_list in bullet_enemy_collisions.items():
            for enemy in enemy_list:
                # Create explosion at the center of the enemy rect
                explosion = Explosion(enemy.rect.center)
                all_sprites.add(explosion)

                # Add power with a 8% chance at the center of the enemy rect
                if random.random() < 0.90:
                    power = Power(enemy.rect.center)
                    all_sprites.add(power)
                    powers.add(power)

        # Check for collisions between bullets and hazards
        bullet_hazard_collisions = pg.sprite.groupcollide(bullets, hazards, True, False, pg.sprite.collide_mask)
        for bullet, hazards_list in bullet_hazard_collisions.items():
            for hazard in hazards_list:
                # Kill bullet if it collides with a hazard
                bullet.kill()
    
    def check_player_hit(self, hazards, enemy_grp, enemy_blt_grp):
        now = pg.time.get_ticks()
        if now - self._last_hit_time > Config.INVULN_WINDOW:
            # enemies or enemy bullets hitting player
            #add code for hit by obstacle, boss, or boss bullet
            hit_by_ship = pg.sprite.spritecollide(self, enemy_grp, True)
            hit_by_bullet = pg.sprite.spritecollide(self, enemy_blt_grp, True)
            hit_by_hazard = pg.sprite.spritecollide(self, hazards, False, pg.sprite.collide_mask)
            # handle collisions
            if hit_by_ship or hit_by_bullet or hit_by_hazard:
                self.add_damage(2)
                self._last_hit_time = now
                # bounce away from hazards
                for hazard in hit_by_hazard:
                    dx, dy = self.rect.centerx - hazard.rect.centerx, self.rect.centery - hazard.rect.centery
                    dist = math.hypot(dx, dy)
                    if dist != 0:
                        self.rect.centerx += dx / dist * 15
                        self.rect.centery += dy / dist * 15
                #todo: kill if not alive
    
    def check_powerup_touched(self, powers):
        #handle powerups!
        touched_powers = pg.sprite.spritecollide(self, powers, True)
        for power in touched_powers:
            if power.get_name() == "pill":
                    self.add_health(2)
            if power.get_name() == "taser":
                if self.level == 3:
                    self.add_health(1)
                elif self.level < 3:
                    if self.level<2:
                        self.shot_delay *= 0.5477
                    self.level+=1
            # add other power-up handling logic here
                   
                
    def blink_ship(self):
        now = pg.time.get_ticks()
        blink_len = 200 # how long each blink lasts
        blink_alpha = 100 # set blink alpha value (0-255)
        
        # only blink the ship if it's currently invulnerable
        if now - self._last_hit_time < Config.INVULN_WINDOW:
            blink_on = (now - self._last_hit_time) % blink_len < blink_len / 2
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

  
    # deals with all of the key inputs
    # directional input, plus space to shoot.
    # calculates acceleration using velocity * friction for smooth movement
    def handle_input(self, all_sprites, bullets):
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
            self.shoot(all_sprites, bullets)
        #calc acceleration
        self.acc.x += self.velocity.x * Config.FRIC
        self.acc.y += self.velocity.y * Config.FRIC
        
   
    def update(self, dt,clock, hazards, all_sprites, bullets, powers, enemy_grp, enemy_blt_grp):
        self.handle_input(all_sprites, bullets)
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
        self.check_enemy_hit(hazards, all_sprites, bullets, enemy_grp, powers)
        self.check_player_hit(hazards, enemy_grp, enemy_blt_grp)
        self.blink_ship()
        self.check_powerup_touched(powers)
        #animate the ship
        self.animation_timer += clock.get_time()
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.images)
            self.image = self.images[self.animation_frame]
            # update the original image
            self.original_image = self.image.copy() 

    def add_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def add_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

        
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
         # can add other things to draw here
        screen.blit(self.images[self.animation_frame], self.rect)

        
        

#    def reset(self):


