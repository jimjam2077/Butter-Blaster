import pygame as pg
from config import Config


# passing Sprite makes Player Class a child of Sprite
# can then use super().__init__() to call the Sprite's init() function

#screen limits - remember window grows down and right 0,0 is top left corner
top_lim = 20
left_lim = 20
bottom_lim = Config.HEIGHT - 20
right_lim = Config.WIDTH - 20
vector = pg.math.Vector2

class Player(pg.sprite.Sprite):
    _instance = None
    
    def __new__(cls): #make the class a singleton - never want multiple player objects
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        super().__init__()
        self.image = pg.image.load("assets/playership.png")
        x_size = self.image.get_width() * 2 # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * 2
        self.image = pg.transform.scale(self.image, (x_size, y_size))
        self.rect = self.image.get_rect()  # defines the borders according to image size
        self.mask = pg.mask.from_surface(self.image) #mask for pixel-perfect collision detection
        
        # set up the position and movement variables
        self.pos = vector((Config.PLAYER_POS))
        self.velocity = vector(0,0)
        self.acc = vector(0,0)
        
        self.rect.center = (Config.PLAYER_POS)  # defines a starting position for rect
        self.initialized = True

    def update(self):
        self.acc = vector(0,0)
        
        pressed_keys = pg.key.get_pressed()
        if (self.rect.top > top_lim):
            if pressed_keys[pg.K_UP] or pressed_keys[pg.K_w]:
                self.acc.y = -Config.ACC
        if (self.rect.bottom < bottom_lim):
            if pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_s]:
                self.acc.y = +Config.ACC
        if (self.rect.left > left_lim): # dont move off screen
            if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_a]:
                self.acc.x = -Config.ACC
        if(self.rect.right < right_lim):
            if pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_d]:
                self.acc.x = +Config.ACC
        # code for spacebar

        #apply friction
        self.acc.x += self.velocity.x * Config.FRIC
        self.acc.y += self.velocity.y * Config.FRIC
        self.velocity += self.acc
        self.pos += self.velocity + 0.5 * self.acc
        
        # update hitbox
        self.rect.center = self.pos

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)

#    def reset(self):
