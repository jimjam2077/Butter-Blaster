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
from gamestates.game_complete import GameComplete
from utils.sprite_handler import SpriteHandler
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
from gamestates.game_over import GameOver
import pygame as pg


class MainLevel(State):
    def __init__(self, game):
        super().__init__(game)
        # all of the entities that make up the game
        self.sprite_handler = SpriteHandler()
        self.player = Player(game.get_pilot())
        self.sprite_handler.add_player(self.player)
        self.sprite_handler.player.reset()
        
        # for calculating how many enemies to spawn and when
        self.start_time = pg.time.get_ticks()
        self.enemy_strength = 1 # update continuously to spawn more mobs
        self.max_strength = 12 # max number of enemies in a wave
    
    
    #TODO: Two main phases: enemy phase -> boss phase
    def update(self, delta_time):
        # player dead? -> game over
        if self.sprite_handler.player.get_score() == 160 and self.sprite_handler.boss is None:
            pg.mixer.music.fadeout(500)
            self.sprite_handler.add_boss(Boss());
            self.sprite_handler.player.increase_score();
            # change the background speed
        # Must handle the QUIT event, else there's an error
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause = Pause(self.game)
                pause.enter_state()
        # spawn some enemies and obstacles randomly, as long as the boss is not alive
        if self.sprite_handler.boss is None:
            self.spawn_enemies()
        else:
            pass # do boss stuff
        #update sprites
        if self.sprite_handler.boss is not None:
            AudioLoader.play_boss_bgm()
        else:
            AudioLoader.play_bgm()   
        self.sprite_handler.update_all_sprites(delta_time)
        self.sprite_handler.check_collisions(delta_time)
        if not self.sprite_handler.player.alive():
            self.game_over()
        if self.sprite_handler.boss is not None and not self.sprite_handler.boss.alive():
            self.sprite_handler.player.reset()
            game_complete = GameComplete(self.game)
            game_complete.enter_state()
            
            
    def render(self, display):
        display.fill((0,0,0))
        self.sprite_handler.background.draw(display)
        self.sprite_handler.all_sprites.draw(display)
        self.sprite_handler.player.update_hud(display)
        if(self.sprite_handler.boss is not None):
            self.sprite_handler.boss.advanced_health(display)
        # render boss hp
        # render score
        pg.display.update()
        

    """def update_all_sprites(self, delta_time):
        self.background.update(delta_time)  
        self.P1.update(delta_time, self.game.clock, self.hazards, self.all_sprites, self.bullets, self.powers, self.enemies, self.enemy_bullets)
        for sprite in self.all_sprites:
            if sprite != self.P1:
                if isinstance(sprite, Enemy):
                    sprite.update(delta_time, self.all_sprites, self.enemies, self.enemy_bullets)
                elif isinstance(sprite, Jena) or isinstance(sprite, Boss):
                    sprite.update(delta_time, self.all_sprites, self.bullets)
                else:
                    sprite.update(delta_time)"""


    def spawn_enemies(self):
        if random.random() <= 0.001*self.enemy_strength:
            hazard = Hazard()
            self.sprite_handler.add_hazard(hazard)
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
            
        if not self.sprite_handler.enemies or len(self.sprite_handler.enemies)<=2: # check for empty
            print("generating enemies!")
            for x in range(random.randint(1,self.enemy_strength)):
                enemy = Enemy()
                self.sprite_handler.add_enemy(enemy)


    def game_over(self):
        AudioLoader.stop_sound()
        explosion = Explosion(self.sprite_handler.player.rect.center)
        self.sprite_handler.all_sprites.add(explosion)
        game_over = GameOver(self.game)
        game_over.enter_state()
        self.sprite_handler.player.reset()
        