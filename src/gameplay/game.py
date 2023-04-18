import sys
import random
import pygame as pg
from config import Config
from components.player import Player
from components.enemy import Enemy
from components.background import Background
from components.power import Power
from components.explosion import Explosion
from utils.asset_loader import AssetLoader
from utils.state import State

class Game:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
    
    #game_state = State.START #updated to track which method here should be called
    #Config.setup_window() # need to set this window up before doing anything in this file
    #screen = Config.SCREEN #the screen object

    # setup sprite groups
    # a sprite added to a group will not be updated in all groups simultaneously when operated on
    # but will be deleted from all groups when kill() is called
    # This might need to be refactored later - it's very important to keep track of these groups
        self._game_state = State.START
        self._screen = Config.SCREEN
        self.P1 =  Player()
        self.background = Background()
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.all_sprites = pg.sprite.Group() # collection of all sprites - potentially don't need this!
        self.all_sprites.add(self.P1)
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)


    # returns the current state of the game
    def get_game_state(self):
        return self._game_state


    def run_start_screen(self, dt):
        Config.setup_window() # need to set this window up before doing anything in this file
        # set up text objects
        # used to display a start up message
        font = AssetLoader.load_story_font(64)
        presenting_text = font.render("BBC PRESENTS...", True, (255, 255, 255))
        presenting_rect = presenting_text.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2))
        # used to display "Press Space" instruction to user
        font = AssetLoader.load_story_font(45)
        start_text = font.render("Press space", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(40+start_text.get_width()/2, Config.HEIGHT -40 -start_text.get_height()/2))
        # splash screen image
        start_img = pg.image.load("assets/title.png").convert_alpha()
        start_img_rect = start_img.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2))
        
        # set up the initial screen
        self._screen.fill(Config.BLK)
        self._screen.blit(presenting_text, presenting_rect)
        pg.display.update()
        pg.time.wait(3000)
        pg.event.clear()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self._game_state = State.CHAR
                    return
            self._screen.blit(start_img, start_img_rect)
            self._screen.blit(start_text, start_rect)      
            pg.display.update()

        
    def run_char_screen(self):
        # create font objects
        title_font = pg.font.Font(None, 64)
        text_font = pg.font.Font(None, 32)
        credit_font = pg.font.Font(None, 20)
        
        # create title text
        title_text = title_font.render("SELECT YOUR PILOT!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(Config.WIDTH/2, 40+title_text.get_height()/2))
        
        # create image rects
        image1_rect = pg.Rect(Config.WIDTH/2 - 400, Config.HEIGHT/2 - 50, 200, 200)
        image2_rect = pg.Rect(Config.WIDTH/2 - 100, Config.HEIGHT/2 - 50, 200, 200)
        image3_rect = pg.Rect(Config.WIDTH/2 + 200, Config.HEIGHT/2 - 50, 200, 200)
        
        # create text objects
        text1 = text_font.render("Dune", True, (255, 255, 255))
        text2 = text_font.render("Toad", True, (255, 255, 255))
        text3 = text_font.render("Jena", True, (255, 255, 255))
        
        # create credit text
        credit_text = credit_font.render("copyright bibleboyschurch",
                                        True, (255, 255, 255))
        credit_rect = credit_text.get_rect(bottomright=(Config.WIDTH-10, Config.HEIGHT-10))
        
        # fill screen with grey
        self._screen.fill((100, 100, 100))
        
        # draw title
        self._screen.blit(title_text, title_rect)
        
        # draw images
        # replace image1.png, image2.png, and image3.png with actual image file names
        image1 = pg.image.load("src/Capture.PNG").convert_alpha()
        image2 = pg.image.load("src/Capture.PNG").convert_alpha()
        image3 = pg.image.load("src/Capture.PNG").convert_alpha()
        self._screen.blit(image1, image1_rect)
        self._screen.blit(image2, image2_rect)
        self._screen.blit(image3, image3_rect)
        
        # draw text
        self._screen.blit(text1, text1.get_rect(center=image1_rect.center).move(0, 150))
        self._screen.blit(text2, text2.get_rect(center=image2_rect.center).move(0, 150))
        self._screen.blit(text3, text3.get_rect(center=image3_rect.center).move(0, 150))
        
        # draw credit
        self._screen.blit(credit_text, credit_rect)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self._game_state = State.STORY # CHANGE THIS LATER ON
                return
        pg.display.update()
        
    def run_story_screen(self):
        text = "Episode I\n\nCROHN'S DISEASE\n\nIt is a time of great unrest in the Kratomite galaxy. The evil Pig King Andy Chan has enslaved the peaceful Kratomites to mine the precious resource Kratom, which he uses to fuel his tyrannical empire.\n\nBut one lone space ranger, armed with nothing but his trusty spaceship and his unwavering determination, has decided to take a stand against the Pig King and his minions.\n\nAs he hurtles through the galaxy at breakneck speeds, the space ranger must navigate treacherous asteroid fields, battle swarms of enemy fighters, and outwit the Pig King's deadliest traps.\n\nBut with each victory, the space ranger grows stronger, more determined, and more confident in his quest to save the Kratomites and put an end to the Pig King's reign of terror once and for all.\n\nBazinga!"
        font = AssetLoader.load_story_font(50)
        skip = 0 # check for number of space presses to skip
        
        lines = []
        for para in text.split('\n\n'):
            words = para.split()
            line = words.pop(0)
            for word in words:
                if font.size(line + ' ' + word)[0] <= 1280:
                    line += ' ' + word
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        
        y = self._screen.get_height()
        while True:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    skip +=1
                    if skip == 2:
                        self._game_state = State.PLAYING
                        return
                

            # Update text position and size
            y -= 0.1
            text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
            text_rects = [text_surface.get_rect(centerx=self._screen.get_rect().centerx, centery=y+64*i) for i, text_surface in enumerate(text_surfaces)]

            # Draw the background and text
            self._screen.fill((0, 0, 0))
            for text_surface, text_rect in zip(text_surfaces, text_rects):
                self._screen.blit(text_surface, text_rect)
            pg.display.update()
        

    def run_game_screen(self, clock):
            # blit() draws the surface to the screen
            # Processing
            # Events
            # Render - need to re-render everything each iteration
            self._screen.fill(Config.BLK)

            # event handling - gets all event from the event queue
            events = pg.event.get()
            for event in events:
                # Must handle the QUIT event, else there's an error
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                    # running = False
            self.background.update()
            self.background.draw(self._screen)
            # generate a new group of enemies if the enemies have been kill()ed
            # kill() removes the sprite from all groups
            # this way i can generate a random number of enemies to attack at a time
            if not self.enemies or len(self.enemies)<=2: # check for empty
                print("generating enemies!")
                for x in range(random.randint(3,10)):
                    e = Enemy()
                    self.enemies.add(e)
                    self.all_sprites.add(e)
            
            #update and draw the sprites!        
            self.P1.update(clock, self.all_sprites, self.bullets, self.enemies, self.enemy_bullets)
            for sprite in self.all_sprites:
                if sprite != self.P1:
                    if isinstance(sprite, Enemy):
                        sprite.update(self.all_sprites, self.enemies, self.enemy_bullets)
                    elif isinstance(sprite, Power) or isinstance(sprite, Explosion):
                        sprite.update(clock)
                    else:
                        sprite.update()
            self.all_sprites.draw(self._screen)
            #debug
            #for sprite in all_sprites:
                #pg.draw.rect(screen, pg.Color("white"), sprite.rect, width=1)
            #pg.display.flip()

                
    def run_game_over():
        print("placeholder")
    
        
    def run_game_won():
        print("placeholder")


    def pause_game():
        print("placeholder")