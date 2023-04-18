# import the pygame module, so you can use it
import pygame as pg
from config import Config
from gameplay.game import Game
from utils.state import State
#from gameplay.game_screens import run_start_screen, run_char_screen, run_story_screen, run_game_screen,  run_game_over, run_game_won, get_game_state
pg.init() # initialize the pygame module

def main():
    clock = pg.time.Clock()
    Config.setup_window()
    game = Game()
    # main loop
    running = True
    clock.tick(Config.FPS)
    last_tick = pg.time.get_ticks()
    while running:
        # calculate delta time in seconds
        current_tick = pg.time.get_ticks()
        dt = (current_tick - last_tick) / 1000.0
        state = game.get_game_state()
        if(state== State.START):
            game.run_start_screen(dt)
        elif(state == State.CHAR):
            game.run_char_screen()
        elif(state == State.STORY):
            game.run_story_screen()
        elif (state == State.PLAYING):
            game.run_game_screen(clock)
        #update display
        pg.display.update()
        last_tick = current_tick
        clock.tick(Config.FPS)
        


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
