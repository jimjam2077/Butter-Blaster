import pygame as pg
# could make this a bit more secure
# but it will do for now!
class Config:
    
    #screen
    FPS = 60;
    WIDTH = 1280
    HEIGHT = 720
    WHT = (255, 255, 255)
    BLKBLU = (0,0,102)
    SCREEN = None

    #movement
    ACC = 1.1
    FRIC = -0.08
    PLAYER_POS = (40, HEIGHT/2) #starting placement offset 40 from left edge
    PLAYER_SCALE = 1
    
    #combat
    SHOT_DELAY = 200
    BULLET_SPEED = 10
    
    @staticmethod
    def setup_window(): #double buffering enabled
        Config.SCREEN = pg.display.set_mode((Config.WIDTH, Config.HEIGHT), vsync=True | pg.HWACCEL | pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption("ANDY'S SNACK ATTACK")  # load and set the logo
        icon = pg.image.load("assets/icon.png")
        pg.display.set_icon(icon)