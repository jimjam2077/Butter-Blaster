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
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        
        self._initialized = True
        #set up the ship image, adjust the scaling here
        self.image = AssetLoader.load_toad_ship()
        #self.scale_image(Config.PLAYER_SCALE)
        self.mask = pg.mask.from_surface(self.image) #mask for pixel-perfect collision detection
        
        # set up the position and movement variables
        self.pos = vector((Config.PLAYER_POS))
        self.velocity = vector(0,0)
        self.acc = vector(0,0)
        self.rect = self.image.get_rect(center=self.pos)  # defines the borders according to image size
        
        # set up the player statistics
        self._last_shot_time = 0 #used to limit fire rate later
        self._lives = 3
    
    
    #property getter for lives 
    @property 
    def lives(self):
        return self._lives
    
    #property setter for lives
    @lives.setter
    def lives(self, count):
        self._lives = count

    def __new__(cls): #make the class a singleton - don't want multiple player objects (for now)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
        
    # use to scale this player by some factor    
    def scale_image(self, factor):
        x_size = self.image.get_width() * factor # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * factor
        self.image = pg.transform.scale(self.image, (x_size, y_size)) # defines a starting position for rect


    def shoot(self, all_sprites, bullets):
        now = pg.time.get_ticks()
        if now - self._last_shot_time > Config.SHOT_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            bullets.add(bullet)
            all_sprites.add(bullet)
            self._last_shot_time = now
            
            
    def get_lives(self):
        return self.lives
    
    def handle_colissions(self, enemy_grp, enemy_blt_grp):
        
        
       
    def update(self, all_sprites, bullets):
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

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)
        

#    def reset(self):


