import asyncio
import math
import os, time
import pygame as pg
# Load our scenes
from src.gamestates.title import Title
from src.config import Config
from src.utils.audio_loader import AudioLoader
from src.utils.asset_loader import AssetLoader

class Main():
        def __init__(self):
            pg.mixer.pre_init(44100, 16, 2, 4096)
            pg.init() # need to do this before other things
            # Set the allowed event types
            pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
            #pg.key.set_repeat(1, 1)  # Enable key repeat for continuous key presses
            self.GAME_W,self.GAME_H = 1280, 720
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1280, 720
            self.game_canvas = pg.Surface((self.GAME_W,self.GAME_H))
            self.screen = Config.setup_window() # set up the window before trying to set up graphics
            AssetLoader.load_assets()
            self.running, self.playing = True, True
            #self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt = 0
            self.prev_time = time.time()
            self.state_stack = []
           # self.load_assets()
            self.load_states()
            self.clock = pg.time.Clock()
            self.pilot = ""

        async def main(self):
            while self.playing:
                self.get_dt()
                #self.get_events()
                self.update()
                self.render()
                #self.clock.tick(Config.FPS)
                await asyncio.sleep(0)

        def update(self):
            self.state_stack[-1].update(self.dt)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pg.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pg.display.flip()


        def get_dt(self):
            self.dt = self.clock.tick(Config.FPS) / 1000

        def get_pilot(self):
            return self.pilot
        
        def set_pilot(self, name):
            self.pilot = name
        
        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)
g = Main()
asyncio.run(g.main())

""" if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop() """