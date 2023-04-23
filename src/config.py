import pygame as pg
# could make this a bit more secure
# but it will do for now!
class Config:
    
    STORY = "Captain, listen up! \n\nI've just received a briefing from Commander Mudkip and the situation is way worse than we feared. The notorious Pig King Andy Chan has invaded Kratomite space, enslaving the peaceful inhabitants and forcing them to mine the precious resource Kratom to fuel his twisted ambitions. And to make things even worse, our intel indicates that due to his excessive snacking and mismanaged Crohn's disease, he's simultaneously causing a food shortage and polluting the sector with... fecal matter! Up until now he'd been working with his sister, but she appears to have moved on to sector M3XC01; giving us the window of opportunity to strike, alright. \n\nHe's deployed an army of Lokomatons to prevent anyone from getting close to him so we've assigned you an agile ship - the Orville Redenbacher Eaglescreech 6900 Butter Cannon...! \n\nBut let me stress; this will not just be an easy mission. You'll most likely be going alone, but you need to keep an eye out for operatives in the area who may be able to lend a hand. \n\nAnd remember: we're not in this for the bits, we're not in here for the donos, we're not going for the subs - we're doing this because it's the right thing to do. The Kratomites are counting on you to free them from Pig King's tyranny, and we won't let them down. \n\nSo stay alert, stay focused, and let's grease that pig! \n\nBazinga, Captain."
    
    #screen
    FPS = 30;
    WIDTH = 1280
    HEIGHT = 720
    WHT = (255, 255, 255)
    BLK = (0,0,0)
    SCREEN = None
    
    #movement
    FRIC = -4
    ACC = 2200
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