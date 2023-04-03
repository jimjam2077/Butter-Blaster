# import the pygame module, so you can use it
import random
import sys
import pygame as pg
import sys
from components.player import Player
from config import Config
from components.enemy import Enemy



def main():
    FrameRate = pg.time.Clock()
    pg.init() # initialize the pygame module
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode((1280, 720), pg.HWSURFACE | pg.DOUBLEBUF)  # w, h
    pg.display.set_caption("PLACEHOLDER")  # load and set the logo
    
    # Surfaces can quickly draw something on the screen
    surface = pg.Surface((20, 20))
    surface.fill((0, 255, 0))  # tuple of RGB values

    P1 =  Player()
    enemies = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(P1)
    
    for x in range(10):
        dorito = Enemy()
        enemies.add(dorito)


    # main loop
    running = True
    hidden_screen = pg.Surface((Config.WIDTH, Config.HEIGHT))
    while running:
        num_to_draw = random.randint(1, len(enemies))  # choose a random number of entities to kill
        hazard_to_draw = random.sample(enemies.sprites(), 2)  # select a random subset of entities to kill
        # blit() draws the surface to the screen
        hidden_screen.fill(Config.WHITE)
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
        P1.draw(hidden_screen)
        for haz in hazard_to_draw:
            haz.draw(hidden_screen)
        
            # Draw the hidden screen to the visible screen
        screen.blit(hidden_screen, (0, 0))
        pg.display.update() #updates the game state
        FrameRate.tick(Config.FPS)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
