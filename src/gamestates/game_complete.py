import random
import sys
from src.gamestates.state import State
from src.config import Config
from src.components.background import Background
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader
import pygame

class GameComplete(State):
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
            "Let's haul this hog off to the Dixie Auction.",
            "LET'S GOOOOOOOO!"
        }
        self.taunt_text = self.font.render(random.choice(tuple(self.lines)), True, (255, 255, 255))
        self.taunt_rect = self.taunt_text.get_rect(midtop = (Config.WIDTH/2, self.port_rect.bottom + 40))
        self.quit_text = self.font.render("Main Menu", True, (255,255,255))
        self.quit_rect = self.quit_text.get_rect(center = (Config.WIDTH/2, self.taunt_rect.bottom + 160))
        # Set up image scaling variables
        self._retry_scaled = False
        self._chars_scaled = False
        self._surfaces = [self.quit_rect]
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
                        if rect == self.quit_rect:
                            from gamestates.title import Title
                            new_state = Title(self.game)
                            new_state.restart()
                            pass

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.overlay, (0,0))
        display.blit(self.portrait, self.port_rect)
        display.blit(self.taunt_text, self.taunt_rect)
        display.blit(self.quit_text, self.quit_rect)
