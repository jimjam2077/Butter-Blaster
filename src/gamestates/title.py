import sys

import pygame as pg

from src.config import Config
from src.gamestates.char_select import CharSelect
from src.gamestates.state import State
from src.utils.asset_loader import AssetLoader
from src.utils.audio_loader import AudioLoader


class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = AssetLoader.fonts["flavour"]
        self.presenting_text = self.font.render("Balding By Choice Studios PRESENTS...", True, (255, 255, 255))
        self.presenting_rect = self.presenting_text.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2))
        # used to display "Press Space" instruction to user
        self.font = AssetLoader.fonts["instruction"]
        self.start_text = self.font.render("Press space", True, (255, 255, 255))
        self.start_text.set_alpha(0)
        self.start_rect = self.start_text.get_rect(center=(100+self.start_text.get_width()/2, Config.HEIGHT -40 -self.start_text.get_height()/2))
        # splash screen image
        self.start_img = AssetLoader.backgrounds["screens"]["title"]
        self.start_img.set_alpha(0)
        self.start_img_rect = self.start_img.get_rect(center=(Config.WIDTH/2, Config.HEIGHT/2))  
        self.alpha = 0
        self.fade_spd = 255 / (3 * 60) # 2 seconds at 60fps
        self.pres_faded_in = False
        self.pres_faded_out = False # maybe i don't need 2 variables for this? revisit
        self.img_faded_in = False
        self.start_faded_out = False
        AssetLoader.music["title"].play(-1, fade_ms=5000)

    def update(self, delta_time):
        if not self.pres_faded_in: # if presenting hasn't displayed, fade it in
            self.fade_in(delta_time, self.presenting_text, "pres_faded_in")
        elif not self.pres_faded_out: # if it has displayed, fade it out
            self.fade_out(delta_time, self.presenting_text, "pres_faded_out")
        if self.pres_faded_out and not self.img_faded_in: # once presenting is gone, fade the image in
            self.fade_in(delta_time, self.start_img, "img_faded_in")
        if self.img_faded_in: # once the image is up...
            self.blink(delta_time, self.start_text)
            
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    # change the value to False, to exit the main loop
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    AudioLoader.stop_sound() # might need to rethink this 
                    new_state = CharSelect(self.game)
                    new_state.enter_state()
                    return


    def render(self, canvas):
        canvas.fill((0,0,0))
        canvas.blit(self.presenting_text, self.presenting_rect)
        canvas.blit(self.start_img, self.start_img_rect)
        canvas.blit(self.start_text, self.start_rect)
        #pg.display.update()
    
    def blink(self, delta_time, surface):
        self.alpha += self.fade_spd * delta_time * 120
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_spd = -abs(self.fade_spd)
        elif self.alpha <= 0:
            self.alpha = 0
            self.fade_spd = abs(self.fade_spd)
        surface.set_alpha(int(self.alpha))          
    
    def fade_in(self, delta_time, surface, faded_variable_name):
        faded_variable = getattr(self, faded_variable_name)
        self.alpha += self.fade_spd * delta_time * 60
        if self.alpha >= 255:
            self.alpha = 255
            setattr(self, faded_variable_name, not faded_variable)
        surface.set_alpha(int(self.alpha))
        #return faded_variable
    
    def fade_out(self, delta_time, surface, faded_variable_name):
        faded_variable = getattr(self, faded_variable_name)
        self.alpha -= self.fade_spd * delta_time * 60
        if self.alpha <= 0:
            self.alpha = 0
            setattr(self, faded_variable_name, not faded_variable)
        surface.set_alpha(int(self.alpha))
        #return faded_variable
    
    # not really used
    def reset(self):
        self.start_text.set_alpha(0)
        self.start_img.set_alpha(0)
        self.alpha = 0        
        self.pres_faded_in = False
        self.pres_faded_out = False # maybe i don't need 2 variables for this? check later
        self.img_faded_in = False
        self.start_faded_out = False
            