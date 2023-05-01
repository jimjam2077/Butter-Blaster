import os, time
import pygame as pg
# Load our scenes
from gamestates.title import Title
from config import Config


class Game():
        def __init__(self):
            pg.init()
            self.GAME_W,self.GAME_H = 1280, 720
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1280, 720
            self.game_canvas = pg.Surface((self.GAME_W,self.GAME_H))
            self.screen = Config.setup_window()
            self.running, self.playing = True, True
            #self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt = 0
            self.prev_time = time.time()
            self.state_stack = []
           # self.load_assets()
            self.load_states()
            self.clock = pg.time.Clock()
            self.pilot = ""

        def game_loop(self):
            while self.playing:
                self.get_dt()
                #self.get_events()
                self.update()
                self.render()
                self.clock.tick(Config.FPS)

        def update(self):
            self.state_stack[-1].update(self.dt)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pg.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pg.display.flip()


        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def get_pilot(self):
            return self.pilot
        
        def set_pilot(self, name):
            self.pilot = name
        
        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()