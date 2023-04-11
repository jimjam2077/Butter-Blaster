import sys
import random
import pygame as pg
from config import Config
from components.player import Player
from components.enemy import Enemy
from utils.state import State

game_state = State.START
screen = Config.SCREEN
# setup sprite groups
P1 =  Player()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(P1)
all_sprites.add(bullets)
all_sprites.add(enemies)
all_sprites.add(enemy_bullets)
# passing sprite groups - every sprite is accessible from 
# all_sprites. for this small game it's easier just to pass the subgroups around
# directly.
    

    
def get_game_state():
    return game_state


def run_start_screen():
    global game_state
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            game_state =  State.PLAYING

def run_game_screen():
        # blit() draws the surface to the screen
        # Processing
        # Events
        # Render - need to re-render everything each iteration
        screen.fill(Config.BLKBLU)

        # event handling - gets all event from the event queue
        events = pg.event.get()
        for event in events:
            # Must handle the QUIT event, else there's an error
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
                # running = False
                
        # generate a new group of enemies if the enemies have been kill()ed
        # kill() removes the sprite from all groups
        # this way i can generate a random number of enemies to attack at a time
        if not enemies or len(enemies)==1: # check for empty
            print("generating enemies!")
            for x in range(random.randint(3,10)):
                e = Enemy()
                enemies.add(e)
                all_sprites.add(e)
        
        #update and draw the sprites!        
        P1.update(all_sprites, bullets)
        for sprite in all_sprites:
            if sprite != P1:
                if isinstance(sprite, Enemy):
                    sprite.update(all_sprites, enemies, bullets)
                else:
                    sprite.update()
        all_sprites.draw(screen)
        #debug
        for sprite in all_sprites:
            pg.draw.rect(screen, pg.Color("white"), sprite.rect, width=1)
        #pg.display.flip()
            
def run_game_over():
    print("placeholder")
    
def run_game_won():
    print("placeholder")


def pause_game():
    print("placeholder")