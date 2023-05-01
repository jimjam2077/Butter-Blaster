import random
import sys
from gamestates.state import State
from config import Config
from components.background import Background
from components.player import Player
from components.enemy import Enemy
from components.explosion import Explosion
from components.power import Power
from components.hazard import Hazard
from components.jena import Jena
from gamestates.pause import Pause
from components.boss import Boss
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
from gamestates.game_over import GameOver
import pygame as pg


class MainLevel(State):
    def __init__(self, game):
        super().__init__(game)
        # all of the entities that make up the game
        self.P1 = Player(game.get_pilot())
        self.P1.reset()
        self.background = Background()
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.powers = pg.sprite.Group()
        self.hazards = pg.sprite.Group()
        self.boss = None
        self.all_sprites = pg.sprite.Group() # collection of all sprites - potentially don't need this!
        self.all_sprites.add(self.P1)
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)
        self.all_sprites.add(self.powers)
        self.all_sprites.add(self.hazards)
        # for calculating how many enemies to spawn and when
        self.start_time = pg.time.get_ticks()
        self.enemy_strength = 1 # update continuously to spawn more mobs
        self.max_strength = 12
    
    
    
    #TODO: Two main phases: enemy phase -> boss phase
    def update(self, delta_time):
        # player dead? -> game over
        if not self.P1.alive():
            self.game_over()
        if self.P1.score == 10:
            self.boss = Boss();
            self.all_sprites.add(self.boss)
            self.P1.score+=1;
        
        # Must handle the QUIT event, else there's an error
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause = Pause(self.game)
                pause.enter_state()
        # spawn some enemies and obstacles randomly, as long as the boss is not alive
        if self.boss is None:
            self.spawn_enemies()
        else:
            pass # do boss stuff
        #update sprites   
        self.update_all_sprites(delta_time)


    def render(self, display):
        display.fill((0,0,0))
        self.background.draw(display)
        self.all_sprites.draw(display)
        self.P1.advanced_health(display)
        if(self.boss is not None):
            self.boss.advanced_health(display)
        # render boss hp
        # render score
        pg.display.update()
        

    def update_all_sprites(self, delta_time):
        self.background.update(delta_time)  
        self.P1.update(delta_time, self.game.clock, self.hazards, self.all_sprites, self.bullets, self.powers, self.enemies, self.enemy_bullets)
        for sprite in self.all_sprites:
            if sprite != self.P1:
                if isinstance(sprite, Enemy):
                    sprite.update(delta_time, self.all_sprites, self.enemies, self.enemy_bullets)
                elif isinstance(sprite, Jena) or isinstance(sprite, Boss):
                    sprite.update(delta_time, self.all_sprites, self.bullets)
                else:
                    sprite.update(delta_time)


    def spawn_enemies(self):
        if random.random() <= 0.001*self.enemy_strength:
            hazard = Hazard()
            self.all_sprites.add(hazard)
            self.hazards.add(hazard)
        if self.enemy_strength > self.max_strength:
            self.enemy_strength = self.max_strength
        else:
            current_time = pg.time.get_ticks() 
            time_since_start = current_time - self.start_time
            if time_since_start >= 10000:  # 10 seconds have passed
                self.enemy_strength += 1
                self.start_time = current_time # update start time
                self.enemy_strength = max(0, min(self.enemy_strength, 10))
            #print(f"Time: {time_since_start / 1000} seconds, Strength: {self.enemy_strength}")
            
        if not self.enemies or len(self.enemies)<=2: # check for empty
            print("generating enemies!")
            for x in range(random.randint(1,self.enemy_strength)):
                e = Enemy()
                self.enemies.add(e)
                self.all_sprites.add(e)


    def game_over(self):
        AudioLoader.stop_sound()
        explosion = Explosion(self.P1.rect.center)
        self.all_sprites.add(explosion)
        game_over = GameOver(self.game)
        game_over.enter_state()
        self.P1.reset()
        