# could make this a bit more secure
# but it will do for now!
class Config:
    FPS = 60;
    
    #screen
    WIDTH = 1280
    HEIGHT = 720
    
    #movement
    ACC = 1.2
    FRIC = -0.1
    PLAYER_POS = (40, HEIGHT/2)
    
    # Predefined some colors
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)