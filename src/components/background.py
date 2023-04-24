import pygame as pg
from utils.asset_loader import AssetLoader

class Background():
      def __init__(self):
            self.img_one = AssetLoader.load_random_bg()
            print(f"img_one: {self.img_one}")
            self.img_two = AssetLoader.load_random_bg()
            print(f"img_two: {self.img_two}")
            self.rect = self.img_one.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rect.width
 
            self.moving_speed = 60
         
      def update(self, dt):
        self.bgX1 -= self.moving_speed * dt
        self.bgX2 -= self.moving_speed * dt
        if self.bgX1 <= -self.rect.width:
            self.bgX1 = self.rect.width
            self.img_one = AssetLoader.load_random_bg()
            print(f"new img_one: {self.img_one.get_at((0,0))}")
        if self.bgX2 <= -self.rect.width:
            self.bgX2 = self.rect.width
            self.img_two = AssetLoader.load_random_bg()
            print(f"new img_two: {self.img_two.get_at((0,0))}")
             
      def draw(self, screen):
         screen.blit(self.img_one, (self.bgX1, self.bgY1))
         screen.blit(self.img_two, (self.bgX2, self.bgY2))

