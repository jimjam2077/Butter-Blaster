import pygame as pg
# could make this a bit more secure
# but it will do for now!
class Config:
    FPS = 60;
    
    #screen
    WIDTH = 1280
    HEIGHT = 720
    
    #movement
    ACC = 1.1
    FRIC = -0.08
    PLAYER_POS = (40, HEIGHT/2)
    
    # Predefined some colors
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Screen object
    SCREEN = None
    
    @staticmethod
    def load_window(): #double buffering enabled
        Config.SCREEN = pg.display.set_mode((Config.WIDTH, Config.HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption("ANDY'S SNACK ATTACK")  # load and set the logo
        icon = pg.image.load("assets/icon.png")
        pg.display.set_icon(icon)