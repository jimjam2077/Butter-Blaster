import random
import sys
from gamestates.state import State
from config import Config
from components.background import Background
from components.player import Player
from components.enemy import Enemy
from components.explosion import Explosion
from components.power import Power
from utils.asset_loader import AssetLoader
import pygame as pg


class MainLevel(State):
    def __init__(self, game):
        super().__init__(game)
        self.P1 = Player(game.get_pilot())
        self.background = Background()
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.all_sprites = pg.sprite.Group() # collection of all sprites - potentially don't need this!
        self.all_sprites.add(self.P1)
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)
    
    def update(self, delta_time):
    
        for event in pg.event.get():
        # Must handle the QUIT event, else there's an error
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
                # running = False
        self.background.update(delta_time)
        
        # generate a new group of enemies if the enemies have been kill()ed
        # kill() removes the sprite from all groups
        # this way i can generate a random number of enemies to attack at a time
        if not self.enemies or len(self.enemies)<=2: # check for empty
            print("generating enemies!")
            for x in range(random.randint(3,10)):
                e = Enemy()
                self.enemies.add(e)
                self.all_sprites.add(e)
        #update and draw the sprites!        
        self.P1.update(delta_time, self.game.clock, self.all_sprites, self.bullets, self.enemies, self.enemy_bullets)
        #check for death, do something, update the 
        for sprite in self.all_sprites:
            if sprite != self.P1:
                if isinstance(sprite, Enemy):
                    sprite.update(delta_time, self.all_sprites, self.enemies, self.enemy_bullets)
                elif isinstance(sprite, Power) or isinstance(sprite, Explosion):
                    sprite.update(self.game.clock)
                else:
                    sprite.update()
        

    def render(self, display):
        display.fill((0,0,0))
        self.background.draw(display)
        self.all_sprites.draw(display)
        pass
        
        