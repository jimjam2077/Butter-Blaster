import pygame as pg
# could make this a bit more secure
# but it will do for now!
class Config:
    
    STORY = "Episode I\n\nCROHN'S DISEASE\n\nIt is a time of great unrest in the Kratomite galaxy. The evil Pig King Andy Chan has enslaved the peaceful Kratomites to mine the precious resource Kratom, which he uses to fuel his tyrannical empire.\n\nBut one lone space ranger, armed with nothing but his trusty spaceship and his unwavering determination, has decided to take a stand against the Pig King and his minions.\n\nAs he hurtles through the galaxy at breakneck speeds, the space ranger must navigate treacherous asteroid fields, battle swarms of enemy fighters, and outwit the Pig King's deadliest traps.\n\nBut with each victory, the space ranger grows stronger, more determined, and more confident in his quest to save the Kratomites and put an end to the Pig King's reign of terror once and for all.\n\nBazinga!"
    
    #screen
    FPS = 60;
    WIDTH = 1280
    HEIGHT = 720
    WHT = (255, 255, 255)
    BLK = (0,0,0)
    SCREEN = None
    
    #movement
    ACC = 1.1
    FRIC = -0.08
    PLAYER_POS = (40, HEIGHT/2) #starting placement offset 40 from left edge
    PLAYER_SCALE = 1
    
    #combat
    PLAYER_LIVES = 3
    INVULN_WINDOW = 3000
    SHOT_DELAY = 200
    BULLET_SPEED = 15
    
    
    @staticmethod
    def setup_window():
        try:
            Config.SCREEN = pg.display.set_mode((Config.WIDTH, Config.HEIGHT), vsync=True | pg.HWACCEL | pg.HWSURFACE | pg.DOUBLEBUF)
        except Exception as e:
            print(f"Error setting up window: {e}")
        pg.display.set_caption("KRATOM CRISIS")  # load and set the logo
        icon = pg.image.load("assets/icon.png")
        pg.display.set_icon(icon)