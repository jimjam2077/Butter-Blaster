import pygame as pg
from components.bullet import Bullet
from config import Config
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
    def __new__(cls): 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        
        self._initialized = True
        #set up the ship image, adjust the scaling here
        self.image = AssetLoader.load_toad_ship()
        self.original_image = self.image.copy()
        # set up the position and movement variables
        self.pos = vector((Config.PLAYER_POS))
        self.velocity = vector(0,0)
        self.acc = vector(0,0)
        self.rect = self.image.get_rect(center=self.pos)  # defines the borders according to image size
        
        # set up the player statistics
        self._last_shot_time = 0 #used to limit fire rate later
        self._last_hit_time = 0 #used for invulnerability window
        self._lives = Config.PLAYER_LIVES
    
    #property getter for lives 
    @property 
    def lives(self):
        return self._lives
    
    #property setter for lives
    @lives.setter
    def lives(self, count):
        self._lives = count
        
        
    # use to scale this player by some factor    
    def scale_image(self, factor):
        x_size = self.image.get_width() * factor # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * factor
        self.image = pg.transform.scale(self.image, (x_size, y_size)) # defines a starting position for rect

    # shoot function - needs to check whether a new bullet can be created
    # there is a delay so that holding spacebar doesn't create a bullet each frame
    # check if the bullet can be fired, then create it and add it to the sprite lists
    def shoot(self, all_sprites, bullets):
        now = pg.time.get_ticks()
        if now - self._last_shot_time > Config.SHOT_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            bullets.add(bullet)
            all_sprites.add(bullet)
            self._last_shot_time = now
            
            
    def get_lives(self):
        return self.lives
    
    
    def handle_collisions(self, bullets, enemy_grp, enemy_blt_grp):
        now = pg.time.get_ticks()
        enemy_killed = pg.sprite.groupcollide(bullets, enemy_grp, True, True)
        if now - self._last_hit_time > Config.INVULN_WINDOW:
            enemy_hit = pg.sprite.spritecollide(self, enemy_grp, True)
            bullet_hit = pg.sprite.spritecollide(self, enemy_blt_grp, True)
            if enemy_hit or bullet_hit:
                self._last_hit_time = now
                self.lives-=1
        
       
    def update(self, all_sprites, bullets, enemy_grp, enemy_blt_grp):
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
        self.velocity += self.acc
        self.pos += self.velocity + 0.5 * self.acc
        
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
        
        # here is just some fluff code to make the ship blink while it's
        # invulnerable (visual player feedback)
        # use blink_len and blink_col to control the speed and colour
        now = pg.time.get_ticks()
        blink_len = 500 # how long each blink lasts
        blink_clr = (255, 100, 0) # set the blink colour
        blink_on = (now - self._last_hit_time) % blink_len < blink_len / 2
        # if the ship is invulnerable, make it blink
        if now - self._last_hit_time < Config.INVULN_WINDOW:
            if blink_on:
                # create a surface with the pixels and fill with blink colour
                fill_pixels = pg.Surface(self.original_image.get_size(), pg.SRCALPHA)
                fill_pixels.fill((blink_clr))
                # multiply RGB values of the surface and source
                fill_pixels.blit(self.original_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
                # blend the resul with the current image - overlays colour on the original image
                fill_pixels.blit(self.image, (0, 0), special_flags=pg.BLEND_RGBA_ADD)
                # set the new filled pixels as the ship image
                self.image.blit(fill_pixels, (0, 0))
                # add a transparency effect
                # self.image.set_colorkey((blink_clr)) 
            else:
                # go back to the original image
                self.image.blit(self.original_image, (0, 0))
        #finally, deal with any collisions
        self.handle_collisions(bullets, enemy_grp, enemy_blt_grp)

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)
        

#    def reset(self):


