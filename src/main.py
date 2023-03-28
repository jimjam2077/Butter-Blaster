# import the pygame module, so you can use it
import sys
import pygame
import sys
from components.player import Player
from config import Config




# define a main function

def main():

    # initialize the pygame module
    pygame.init()

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1280, 720))  # w, h
    # load and set the logo
    pygame.display.set_caption("PLACEHOLDER")
    # Surfaces can quickly draw something on the screen
    background = pygame.Surface((400,300))
    surface = pygame.Surface((20, 20))
    surface.fill((0, 255, 0))  # tuple of RGB values
    pos = [175, 125]
    
    player =  Player()

    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        # Processing
        # Events
        # Render - need to re-render everything each iteration

        # event handling - gets all event from the event queue
        events = pygame.event.get()
        for event in events:
            # Must handle the QUIT event, else there's an error
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
                # running = False
        player.update()
        # blit() draws the surface to the screen
        screen.fill(Config.WHITE)
        player.draw(screen)
        
        pygame.display.update() #updates the game state


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
