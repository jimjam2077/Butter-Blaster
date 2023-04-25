import random
import sys
from gamestates.state import State
from config import Config
from components.background import Background
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
import pygame as pg

class GameOver(State):
    def __init__(self, game):
        super().__init__(game)
        # graphics
        self.overlay = pg.Surface((Config.WIDTH, Config.HEIGHT))
        self.overlay.set_alpha(150)  # Set alpha to 128 (half-transparent)
        self.overlay.fill((0, 0, 0))  # Fill with black color
        self.portrait = AssetLoader.load_avatar("wes")
        self.port_rect = self.portrait.get_rect(midtop=(Config.WIDTH/2, 80))
        # text elements
        self.font = AssetLoader.load_story_font(34)
        self.lines = {
            "Well... guess that's it.",
            "You don't even do anything in this crew.",
            "Are you watching Fishtank?",
            "Alright, I'm coming to get you."
        }
        self.taunt_text = self.font.render(random.choice(tuple(self.lines)), True, (255, 255, 255))
        self.taunt_rect = self.taunt_text.get_rect(midtop = (Config.WIDTH/2, self.port_rect.bottom + 40))
        self.retry_text = self.font.render("Retry", True, (255,255,255))
        self.retry_rect = self.retry_text.get_rect(midright = (Config.WIDTH/2 - 160, self.taunt_rect.bottom + 160))
        self.char_text = self.font.render("Quit", True, (255,255,255))
        self.char_rect = self.char_text.get_rect(midleft = (Config.WIDTH/2 + 160, self.taunt_rect.bottom + 160))
        

    def update(self, delta_time):
        print(len(self.game.state_stack))
        for event in pg.event.get():
        # Must handle the QUIT event, else there's an error
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                from gamestates.main_level import MainLevel
                new_state = MainLevel(self.game)
                new_state.reset_game()   

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.overlay, (0,0))
        display.blit(self.portrait, self.port_rect)
        display.blit(self.taunt_text, self.taunt_rect)
        display.blit(self.retry_text, self.retry_rect)
        display.blit(self.char_text, self.char_rect)
