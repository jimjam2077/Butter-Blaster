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
from utils.audio_loader import AudioLoader

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
        self.background = Background()
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.all_sprites = pg.sprite.Group() # collection of all sprites - potentially don't need this!
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)

    # returns the current state of the game
    def get_game_state(self):
        return self._game_state
    
    def set_state(new_state):
        Game._instance = new_state


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
        AudioLoader.play_start_music()   
        alpha = 0
        fade_spd = 255 / (8 * 60)
        fade_in = True
        fade_out = False
        fade_in_complete = False
        fade_out_complete = False
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    AudioLoader.stop_sound()
                    self._game_state = State.CHAR
                    return
            
            self._screen.fill(Config.BLK)
            
            if fade_in:
                    alpha += fade_spd * dt
                    if alpha >= 255:
                        alpha = 255
                        fade_in_complete = True
                    presenting_text.set_alpha(int(alpha))
                    self._screen.blit(presenting_text, presenting_rect)

            if fade_out:
                alpha -= fade_spd * dt
                if alpha <= 0:
                    alpha = 0
                    fade_out_complete = True
                presenting_text.set_alpha(int(alpha))
                self._screen.blit(presenting_text, presenting_rect)

            if fade_in_complete and fade_out_complete:
                fade_in = False
                fade_out = False
                fade_in_complete = False
                fade_out_complete = False

            if not fade_in and not fade_out:
                # switch to next game state
                self._game_state = State.CHAR
                return

            # this is broken because each frame  this method is called in main, alpha is reset to 0 and all of the ifs are skipped
            # need to preserve the value of alpha to be able to use it
            
            self._screen.blit(start_img, start_img_rect)
            self._screen.blit(start_text, start_rect)
            pg.display.update()
        
    def run_char_screen(self):
        # build the assets
        AudioLoader.play_menu_music()
        # create font objects
        title_font = AssetLoader.load_story_font(64)
        # load images
        toad_img = AssetLoader.load_avatar("toad")
        dune_img = AssetLoader.load_avatar("dune")
        jena_img = AssetLoader.load_avatar("jena")     
        # create image rects
        toad_rect = toad_img.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2)) # place centrally
        dune_rect = dune_img.get_rect(center=toad_rect.center).move(-300, 0) # left of toad
        jena_rect = jena_img.get_rect(center=toad_rect.center).move(300, 0) # left of toad
        characters = {
            "toad": toad_rect,
            "dune": dune_rect
        }
        # create title text
        title_text = title_font.render("SELECT YOUR PILOT", True, pg.Color("firebrick2"))
        title_rect = title_text.get_rect(center=toad_rect.center).move(0, -250)
        # create nameplates
        dune_name = AssetLoader.load_nameplate("dune")
        toad_name = AssetLoader.load_nameplate("toad")
        jena_name = AssetLoader.load_nameplate("jena")
        d_n_rect = dune_name.get_rect(center=dune_rect.center).move(0, 150)
        t_n_rect = toad_name.get_rect(center=toad_rect.center).move(0, 150)
        j_n_rect = jena_name.get_rect(center=jena_rect.center).move(0, 150)
        # create background 
        bg = AssetLoader.load_char_bg()
        bg_rect = bg.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # iterate over characters dictionary to check if a rectangle has been clicked
                for char_name, char_rect in characters.items():
                    if char_rect.collidepoint(pg.mouse.get_pos()):
                        AudioLoader.stop_sound() 
                        self._game_state = State.STORY 
                        self.P1 = Player(char_name) 
                        self.all_sprites.add(self.P1)
                        break #exit the loop
                    
        if toad_rect.collidepoint(pg.mouse.get_pos()):
            # Scale image by 10%
            toad_img, toad_rect = self.scale_on_mouseover(AssetLoader.load_avatar("toad"), toad_rect, 1.1)
        else:
            # Reset image to original size
            toad_img, toad_rect = AssetLoader.load_avatar("toad"), toad_img.get_rect(center=toad_rect.center)

        if dune_rect.collidepoint(pg.mouse.get_pos()):
            # Scale image by 10%
            dune_img, dune_rect = self.scale_on_mouseover(AssetLoader.load_avatar("dune"), dune_rect, 1.1)
        else:
            # Reset image to original size
            dune_img, dune_rect = AssetLoader.load_avatar("dune"), dune_img.get_rect(center=dune_rect.center)

    
        #start drawing. draw base elements at the top
        self._screen.fill((100, 100, 100)) # fill screen
        self._screen.blit(bg, bg_rect) # draw the background
        self._screen.blit(title_text, title_rect) # draw title
        self._screen.blit(dune_img, dune_rect) # draw the portraits
        self._screen.blit(toad_img, toad_rect)
        self._screen.blit(jena_img, jena_rect)
        self._screen.blit(dune_name, d_n_rect) #draw the text relative to the images
        self._screen.blit(toad_name, t_n_rect)
        self._screen.blit(jena_name, j_n_rect)

        pg.display.update()
        
        
    def run_story_screen(self):
        font_size = 46
        spacing = 1.3 # used to detemine how squished the font is
        AudioLoader.play_story_audio()
        wes_img = AssetLoader.load_avatar("wes")
        wes_img = pg.transform.scale(wes_img, (int(wes_img.get_width() * 0.75), int(wes_img.get_height() * 0.75)))
        wes_rect = wes_img.get_rect(topleft = (5, 5))
        text = Config.STORY
        font = AssetLoader.load_story_font(46)
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
            y -= 0.13 #sets the scroll speed
            text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines] # render each line as a surface
            # create rects using the text surface positions
            # the y position is determined by the y + fontsize * line no
            text_rects = [text_surface.get_rect(centerx=self._screen.get_rect().centerx, centery=y+(font_size*spacing)*i) for i, text_surface in enumerate(text_surfaces)]
            
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    skip +=1
                    if skip == 2 or text_rects[-1].y < Config.HEIGHT/2: # change if the last line went offscreen or player skipped
                        AudioLoader.stop_sound()
                        self._game_state = State.PLAYING
                        return
            #update the screen
            self._screen.fill((0, 0, 0))
            if text_rects[-1].y < Config.HEIGHT/2: #move on if the text has fully moves off screen
                cont_txt = font.render("Press Space to Continue", True, (255,255,255))
                cont_rect = cont_txt.get_rect(center=(Config.WIDTH/2, Config.HEIGHT -40 -cont_txt.get_height()/2))
                self._screen.blit(cont_txt, cont_rect)
            for text_surface, text_rect in zip(text_surfaces, text_rects):
                self._screen.blit(text_surface, text_rect)
            self._screen.blit(wes_img, wes_rect)
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
            #check for death, do something, update the 
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
        

    def scale_on_mouseover(self, image, rect, scale_factor):
        # Calculate the new size for the image
        new_size = (int(rect.width * scale_factor), int(rect.height * scale_factor))
        # Scale the image
        scaled_image = pg.transform.scale(image, new_size)
        # Calculate the new rect with the same center as the original rect
        new_rect = scaled_image.get_rect(center=rect.center)
        # Return the scaled image and rect
        return scaled_image, new_rect