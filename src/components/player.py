import pygame as pg
from config import Config


# passing Sprite makes Player Class a child of Sprite
# can then use super().__init__() to call the Sprite's init() function


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load("assets/playership.png")
        x_size = self.image.get_width() * 2 # adjust for scaling of image - possibly make it % of screen
        y_size = self.image.get_height() * 2
        self.image = pg.transform.scale(self.image, (x_size, y_size))
        self.rect = self.image.get_rect()  # defines the borders according to image size
        self.rect.center = (40, Config.HEIGHT/2)  # defines a starting position for rect
        self.mask = pg.mask.from_surface(self.image) #mask for pixel-perfect collision detection
        

    def update(self):
        #screen limits - remember window grows down and right 0,0 is top left corner
        top_lim = 20
        left_lim = 20
        bottom_lim = Config.HEIGHT - 20
        right_lim = Config.WIDTH - 20
        
        
        pressed_keys = pg.key.get_pressed()
        if (self.rect.top > top_lim):
            if pressed_keys[pg.K_UP] or pressed_keys[pg.K_w]:
                self.rect.move_ip(0, -5)  # y grows down, x grows right
        if (self.rect.bottom < bottom_lim):
            if pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_s]:
                self.rect.move_ip(0, 5)
        if (self.rect.left > left_lim): # dont move off screen
            if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_a]:
                self.rect.move_ip(-5, 0)
        if(self.rect.right < right_lim):
            if pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_d]:
                self.rect.move_ip(5, 0)


    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)

#    def reset(self):
