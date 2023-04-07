import pygame as pg
# could make this a bit more secure
# but it will do for now!
class Config:
    
    #screen
    FPS = 60;
    WIDTH = 1280
    HEIGHT = 720
    WHITE = (255, 255, 255)
    SCREEN = None

    #movement
    ACC = 1.1
    FRIC = -0.08
    PLAYER_POS = (40, HEIGHT/2) #starting placement offset 40 from left edge
    
    @staticmethod
    def setup_window(): #double buffering enabled
        Config.SCREEN = pg.display.set_mode((Config.WIDTH, Config.HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption("ANDY'S SNACK ATTACK")  # load and set the logo
        icon = pg.image.load("assets/icon.png")
        pg.display.set_icon(icon)