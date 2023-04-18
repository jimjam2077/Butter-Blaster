# import the pygame module, so you can use it
import pygame as pg
from config import Config
from utils.state import State


def main():
    clock = pg.time.Clock()
    pg.init() # initialize the pygame module
    
    
    # create a surface on screen that has the size of 240 x 180
    #screen = pg.display.set_mode((1280, 720), pg.HWSURFACE | pg.DOUBLEBUF)  # w, h
    Config.setup_window()
    from gameplay.game_screens import run_start_screen, run_char_screen, run_story_screen, run_game_screen,  run_game_over, run_game_won, get_game_state




    # main loop
    running = True
    clock.tick(Config.FPS)
    last_tick = pg.time.get_ticks()
    while running:
        # calculate delta time in seconds
        current_tick = pg.time.get_ticks()
        dt = (current_tick - last_tick) / 1000.0
        state = get_game_state()
        if(state== State.START):
            run_start_screen(dt)
        elif(state == State.CHAR):
            run_char_screen()
        elif (state == State.PLAYING):
            run_game_screen(clock)
        #update display
        pg.display.update()
        last_tick = current_tick
        clock.tick(Config.FPS)
        


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
