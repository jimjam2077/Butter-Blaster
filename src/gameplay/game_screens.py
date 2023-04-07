import sys
import random
import pygame as pg
from config import Config
from components.player import Player
from components.enemy import Enemy


P1 =  Player()
enemies = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(P1)
    
for x in range(10):
    dorito = Enemy()
    enemies.add(dorito)


def run_start_screen():
    print("placeholder")

def run_game_screen():
        num_to_draw = random.randint(1, len(enemies))  # choose a random number of entities to kill
        hazard_to_draw = random.sample(enemies.sprites(), 2)  # select a random subset of entities to kill
        # blit() draws the surface to the screen
        Config.SCREEN.fill(Config.WHITE)
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
        P1.update()
        # Call the kill method on each entity in the subset
        enemies.update()
        P1.draw(Config.SCREEN)
        for haz in hazard_to_draw:
            haz.draw(Config.SCREEN)
    
def run_game_over():
    print("placeholder")
    
def run_game_won():
    print("placeholder")


def pause_game():
    print("placeholder")