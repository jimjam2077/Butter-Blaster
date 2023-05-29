import random
import sys
from src.gamestates.state import State
from src.components.player import Player
from src.components.enemy import Enemy
from src.components.explosion import Explosion
from src.components.hazard import Hazard
from src.gamestates.pause import Pause
from src.components.boss import Boss
from src.gamestates.game_complete import GameComplete
from src.components.turret import Turret
from src.utils.sprite_handler import SpriteHandler
from src.utils.audio_loader import AudioLoader
from src.gamestates.game_over import GameOver
import pygame as pg

from src.utils.asset_loader import AssetLoader


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
        self.transition_surf = pg.Surface((1280, 720)).convert_alpha()
        self.transition_surf.fill((0, 0, 0))
        self.transition_surf.set_alpha(0)
        self.transition_time = 2
        AssetLoader.play_bgm("bgm")
    
    #TODO: Two main phases: enemy phase -> boss phase
    def update(self, delta_time):
        # player dead? -> game over
        if self.sprite_handler.player.get_score() == 3 and self.sprite_handler.boss is None:
            pg.mixer.music.fadeout(1000)
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
            AssetLoader.play_bgm("boss")   
        else:
            AssetLoader.play_bgm("bgm")   
        self.sprite_handler.update_all_sprites(delta_time)
        self.sprite_handler.check_collisions(delta_time)
        if not self.sprite_handler.player.alive():
            self.game_over()
        if self.sprite_handler.boss is not None and not self.sprite_handler.boss.is_alive():
            self.victory_sequence(delta_time)
            
            
    def render(self, display):
        display.fill((0,0,0))
        self.sprite_handler.background.draw(display)
        self.sprite_handler.all_sprites.draw(display)
        self.sprite_handler.player.update_hud(display)
        if(self.sprite_handler.boss is not None):
            self.sprite_handler.boss.advanced_health(display)
        

    def spawn_enemies(self):
        if random.random() <= 0.0005*self.enemy_strength:
            hazard = Hazard()
            self.sprite_handler.add_hazard(hazard)
        if random.random() <= 0.0005*self.enemy_strength:
            turret = Turret()
            self.sprite_handler.add_hazard(turret)
        if self.enemy_strength > self.max_strength:
            self.enemy_strength = self.max_strength
        else:
            current_time = pg.time.get_ticks() 
            time_since_start = current_time - self.start_time
            if time_since_start >= 10000:  # 10 seconds have passed
                self.enemy_strength += 1
                self.start_time = current_time # update start time
                self.enemy_strength = max(0, min(self.enemy_strength, 10))
            
        if not self.sprite_handler.enemies or len(self.sprite_handler.enemies)<=2: # check for empty
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
        
    def victory_sequence(self, delta_time):
        self.transition_time -= delta_time
        if self.transition_time > 0:
            pass
        else: 
            self.sprite_handler.player.reset()
            game_complete = GameComplete(self.game)
            game_complete.enter_state()
    