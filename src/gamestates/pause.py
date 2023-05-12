import random
import sys
from gamestates.state import State
from config import Config
from components.background import Background
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
import pygame as pg

class Pause(State):
    def __init__(self, game):
        super().__init__(game)
        # graphics
        self.overlay = pg.Surface((Config.WIDTH, Config.HEIGHT))
        self.overlay.set_alpha(150)  # Set alpha to 128 (half-transparent)
        self.overlay.fill((0, 0, 0))  # Fill with black color
        self.font = AssetLoader.load_story_font(34)
        self.text = self.font.render("Paused", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center = (Config.WIDTH/2, Config.HEIGHT/2))
        

    def update(self, delta_time):
        for event in pg.event.get():
        # Must handle the QUIT event, else there's an error
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.exit_state()

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.overlay, (0,0))
        display.blit(self.text, self.text_rect)