import pygame as pg
from config import Config


# passing Sprite makes Player Class a child of Sprite
# can then use super().__init__() to call the Sprite's init() function


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load("assets/playership.png")  # add image here
        self.rect = self.image.get_rect()  # defines the borders according to image size
        self.rect.center = (40, Config.HEIGHT/2)  # defines a starting position for rect

    def update(self):
        pressed_keys = pg.key.get_pressed()
        if (self.rect.top > 20):
            if pressed_keys[pg.K_UP]:
                self.rect.move_ip(0, -5)  # y grows down, x grows right
        if (self.rect.bottom < Config.HEIGHT - 20):
            if pressed_keys[pg.K_DOWN]:
                self.rect.move_ip(0, 5)
        if (self.rect.left > 20): # dont move off screen
            if pressed_keys[pg.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if(self.rect.right < Config.WIDTH - 20):
            if pressed_keys[pg.K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)

#    def reset(self):
