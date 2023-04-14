import os
import random
import pygame as pg
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
ASSET_DIR = ROOT_DIR / "assets"
BG_DIR = ASSET_DIR / "bg"
BULLET_DIR = ASSET_DIR / "bullets"
HAZARD_DIR = ASSET_DIR / "hazards"
POWER_DIR = ASSET_DIR / "powers"
EXPLO_DIR = ASSET_DIR / "explosions"
UI_DIR = ASSET_DIR / "ui"
SPRITE_DIR = ASSET_DIR / "sprites"
TOAD_DIR = SPRITE_DIR / "toad"
DUNE_DIR = SPRITE_DIR / "dune"

# this could be a bunch of static variables
# i.e. PLAYER_SHIP = pygame.image.load(file).convert_alpha()
# however, it would mean more memory overhead as everything is loaded at once
# doing it this way means assets are loaded as they are needed
# not really a big concern because this is a tiny game
class AssetLoader:
    
    # loads in all of the sprites for the animated toad ship
    @staticmethod
    def load_toad_ship():
        sprite_count = len(os.listdir(TOAD_DIR))
        images = []
        for i in range(1, sprite_count):
            image_path = TOAD_DIR / f"toadship{i}.png"
            image = pg.image.load(str(image_path)).convert_alpha()
            images.append(image)
        return images
    
    # loads in all of the sprites for the animated dune ship
    @staticmethod
    def load_dune_ship():
        sprite_count = len(os.listdir(DUNE_DIR))
        images = []
        for i in range(1, sprite_count):
            image_path = DUNE_DIR / f"duneship{i}.png"
            image = pg.image.load(str(image_path)).convert_alpha()
            images.append(image)
        return images
    
    # sprites from https://opengameart.org/content/pixel-explosion-12-frames
    # licensed under Creative Commons 3.0
    @staticmethod 
    def load_explosion():
        sprite_count = len(os.listdir(EXPLO_DIR))
        images = []
        for i in range(1, sprite_count):
            image_path = EXPLO_DIR / f"explode{i}.png"
            image = pg.image.load(str(image_path)).convert_alpha()
            images.append(image)
        return images
    
    # want to randomly select an enemy sprite each time, out of the available enemy files
    # need to use joinpath() here because SPRITE_DIR / returns a WindowsPath object
    # which can't be concatenated properly using +
    @staticmethod
    def load_enemy_ship():
        #count up how many sprites are in the power folder
        sprite_count = len([filename for filename in os.listdir(SPRITE_DIR) if os.path.isfile(os.path.join(SPRITE_DIR, filename))])
        return pg.image.load(SPRITE_DIR.joinpath("enemy" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()
    
    # loads up a random background image
    @staticmethod
    def load_random_bg():
        #count up how many sprites are in the power folder
        bg_count = len(os.listdir(BG_DIR))
        return pg.image.load(BG_DIR.joinpath("bg" + str(random.randint(1,bg_count)) + ".png")).convert_alpha()
    
    @staticmethod
    def load_player_bullet():
        return pg.image.load(BULLET_DIR / "playerbullet.png").convert_alpha()
    
    @staticmethod
    def load_enemy_bullet():
        return pg.image.load(BULLET_DIR / "enemybullet.png").convert_alpha()
    
    #load boss 
    
    #load boss projectile
    
    #load 
    
    # load a random power sprite
    @staticmethod
    def load_powerup():
        #count up how many sprites are in the power folder
        sprite_count = len(os.listdir(POWER_DIR))
        return pg.image.load(POWER_DIR.joinpath("power" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()
    