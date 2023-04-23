import sys
from gamestates.state import State
from config import Config
from components.background import Background
from gamestates.main_level import MainLevel
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
import pygame as pg

class StoryScroll(State):
    def __init__(self, game):
        super().__init__(game)
        self._font_size = 46
        self._spacing = 1.3 # used to detemine how squished the font is
        self._wes_img = AssetLoader.load_avatar("wes")
        self._wes_img = pg.transform.scale(self._wes_img, (int(self._wes_img.get_width() * 0.75), int(self._wes_img.get_height() * 0.75)))
        self._wes_rect = self._wes_img.get_rect(topleft = (5, 5))
        self._text = Config.STORY
        self._font = AssetLoader.load_story_font(46)
        self._skip = 0 # check for number of space presses to skip
        self._lines = []
        # split the text up according to screen width
        for para in self._text.split('\n\n'):
            words = para.split()
            line = words.pop(0)
            for word in words:
                if self._font.size(line + ' ' + word)[0] <= 1180: # adjust for line width
                    line += ' ' + word
                else:
                    self._lines.append(line)
                    line = word
            self._lines.append(line)
        self._y = Config.HEIGHT
        self._text_surfaces = [self._font.render(line, True, (255, 255, 255)) for line in self._lines] #used to store individual line renders
        self._text_rects = [text_surface.get_rect(centerx=Config.WIDTH/2, centery=self._y+(self._font_size*self._spacing)*i) for i, text_surface in enumerate(self._text_surfaces)]
        AudioLoader.play_story_audio()
        
    def update(self, delta_time):
        print(delta_time)
        self._y -= 0.6 #sets the scroll speed
        self._text_surfaces = [self._font.render(line, True, (255, 255, 255)) for line in self._lines] # render each line as a surface
        # create rects using the text surface positions
        # the y position is determined by the y + fontsize * line no
        self._text_rects = [text_surface.get_rect(centerx=Config.WIDTH/2, centery=self._y+(self._font_size*self._spacing)*i) for i, text_surface in enumerate(self._text_surfaces)]
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self._skip +=1
                if self._skip == 2 or self._text_rects[-1].y < Config.HEIGHT/2: # change if the last line went offscreen or player skipped
                    AudioLoader.stop_sound()
                    new_state = MainLevel(self.game)
                    new_state.enter_state()
                    return
        
    def render(self, display):
        display.fill((0, 0, 0))
        if self._text_rects[-1].y < Config.HEIGHT/2: #move on if the text has fully moves off screen
            cont_txt = self._font.render("Press Space to Continue", True, (255,255,255))
            cont_rect = cont_txt.get_rect(center=(Config.WIDTH/2, Config.HEIGHT -40 -cont_txt.get_height()/2))
            display.blit(cont_txt, cont_rect)
        for text_surface, text_rect in zip(self._text_surfaces, self._text_rects):
            display.blit(text_surface, text_rect)
        display.blit(self._wes_img, self._wes_rect)
        pg.display.update()