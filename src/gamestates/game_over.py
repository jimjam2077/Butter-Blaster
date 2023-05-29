import random
import sys
from src.gamestates.state import State
from src.config import Config
from src.components.background import Background
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader
import pygame

class GameOver(State):
    def __init__(self, game):
        super().__init__(game)
        # graphics
        self.overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        #self.overlay.set_alpha(150)  # Set alpha to 128 (half-transparent)
        self.overlay.fill((0, 0, 0))  # Fill with black color
        self.portrait = AssetLoader.ui_parts["portraits"]["wes"]
        self.port_rect = self.portrait.get_rect(midtop=(Config.WIDTH/2, 80))
        # text elements
        self.font = AssetLoader.fonts["flavour"]
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
        self.quit_text = self.font.render("Quit", True, (255,255,255))
        self.quit_rect = self.quit_text.get_rect(midleft = (Config.WIDTH/2 + 160, self.taunt_rect.bottom + 160))
        # Set up image scaling variables
        self._retry_scaled = False
        self._chars_scaled = False
        self._surfaces = [self.retry_rect, self.quit_rect]
        #pygame.mixer.stop()
        #pygame.mixer.music.stop()
        AudioLoader.play_end_music()

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # iterate over characters dictionary to check if a rectangle has been clicked
                for rect in self._surfaces:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                        if rect == self.retry_rect:
                            from src.gamestates.main_level import MainLevel
                            new_state = MainLevel(self.game)
                            new_state.reset_game()   
                            pass
                        elif rect == self.quit_rect:
                            from src.gamestates.title import Title
                            new_state = Title(self.game)
                            new_state.restart()
                            pass
        

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.overlay, (0,0))
        display.blit(self.portrait, self.port_rect)
        display.blit(self.taunt_text, self.taunt_rect)
        display.blit(self.retry_text, self.retry_rect)
        display.blit(self.quit_text, self.quit_rect)
