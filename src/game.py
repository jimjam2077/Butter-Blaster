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

        """ def get_events(self):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.playing = False
                        self.running = False
                    if event.key == pg.K_a:
                        self.actions['left'] = True
                    if event.key == pg.K_d:
                        self.actions['right'] = True
                    if event.key == pg.K_w:
                        self.actions['up'] = True
                    if event.key == pg.K_s:
                        self.actions['down'] = True
                    if event.key == pg.K_p:
                        self.actions['action1'] = True
                    if event.key == pg.K_o:
                        self.actions['action2'] = True    
                    if event.key == pg.K_RETURN:
                        self.actions['start'] = True  

                if event.type == pg.KEYUP:
                    if event.key == pg.K_a:
                        self.actions['left'] = False
                    if event.key == pg.K_d:
                        self.actions['right'] = False
                    if event.key == pg.K_w:
                        self.actions['up'] = False
                    if event.key == pg.K_s:
                        self.actions['down'] = False
                    if event.key == pg.K_p:
                        self.actions['action1'] = False
                    if event.key == pg.K_o:
                        self.actions['action2'] = False
                    if event.key == pg.K_RETURN:
                        self.actions['start'] = False """  

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
        
        """ def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            self.font_dir = os.path.join(self.assets_dir, "font")
            self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20) """

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        """def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False """


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()