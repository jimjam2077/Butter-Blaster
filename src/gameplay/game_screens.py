import sys
import random
import pygame as pg
from config import Config
from components.player import Player
from components.enemy import Enemy
from utils.state import State

game_state = State.START
P1 =  Player()
enemies = pg.sprite.Group()
bullets = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(enemies)
all_sprites.add(P1)
all_sprites.add(bullets)
    
for x in range(10):
    e = Enemy()
    enemies.add(e)
    all_sprites.add(e)
    
def get_game_state():
    return game_state


def run_start_screen():
    global game_state
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            game_state =  State.PLAYING

def run_game_screen():
        screen = Config.SCREEN
        hazard_to_draw = random.sample(enemies.sprites(), 2)  # select a random subset of entities to kill
        # blit() draws the surface to the screen
        screen.fill(Config.BLKBLU)
        # Processing
        # Events
        # Render - need to re-render everything each iteration

        # event handling - gets all event from the event queue
        events = pg.event.get()
        for event in events:
            # Must handle the QUIT event, else there's an error
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
                # running = False
        #update and draw the sprites!        
        P1.update(all_sprites)
        for sprite in all_sprites:
            if sprite != P1:
                if isinstance(sprite, Enemy):
                    sprite.update(enemies)
                else:
                    sprite.update()
        all_sprites.draw(screen)
    
def run_game_over():
    print("placeholder")
    
def run_game_won():
    print("placeholder")


def pause_game():
    print("placeholder")