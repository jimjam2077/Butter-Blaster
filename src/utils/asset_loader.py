import os
import random
import pygame as pg
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
ASSET_DIR = ROOT_DIR / "assets"
#under assets
BG_DIR = ASSET_DIR / "bg"
BULLET_DIR = ASSET_DIR / "bullets"
HAZARD_DIR = ASSET_DIR / "hazards"
POWER_DIR = ASSET_DIR / "powers"
EXPLO_DIR = ASSET_DIR / "explosions"
FONT_DIR = ASSET_DIR / "fonts"
UI_DIR = ASSET_DIR / "ui"
SPRITE_DIR = ASSET_DIR / "entities"
#under entities
TOAD_DIR = SPRITE_DIR / "toad"
DUNE_DIR = SPRITE_DIR / "dune"
ENEMY_DIR = SPRITE_DIR / "enemy"

# this could be a bunch of static variables
# i.e. PLAYER_SHIP = pygame.image.load(file).convert_alpha()
# however, it would mean more memory overhead as everything is loaded at once
# doing it this way means assets are loaded as they are needed
# not really a big concern because this is a tiny game
class AssetLoader:
    
    # TODO: refactor these ship loading methods - can just pass in the filename variable
    # sprite_count = len(os.listdir(DIR))
    # image_path = DIR / f"name"+"ship{i}.png"
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
    
    @staticmethod
    def load_player_ship(name):
        dir = SPRITE_DIR / name
        sprite_count = len(os.listdir(dir))
        images = []
        for i in range(1, sprite_count):
            img_path = dir / f"{name}ship{i}.png"
            img = pg.image.load(str(img_path)).convert_alpha()
            images.append(img)
        return images
        
    
    #load the sprites for the animated dune ship
    @staticmethod
    def load_dune_ship():
        sprite_count = len(os.listdir(DUNE_DIR))
        images = []
        for i in range(1, sprite_count):
            image_path = DUNE_DIR / f"duneship{i}.png"
            image = pg.image.load(str(image_path)).convert_alpha()
            images.append(image)
        return images
    
    # load the explosion sprites into an array
    @staticmethod 
    def load_explosion():
        sprite_count = len(os.listdir(EXPLO_DIR))
        images = []
        for i in range(1, sprite_count):
            image_path = EXPLO_DIR / f"explode{i}.png"
            image = pg.image.load(str(image_path)).convert_alpha()
            images.append(image)
        return images
    
    @staticmethod
    def load_avatar(name):
        ava_path = UI_DIR / f"{name}.png"
        return pg.image.load(str(ava_path)).convert_alpha()
    
    @staticmethod
    def load_nameplate(name):
        ava_path = UI_DIR / f"{name}txt.png"
        return pg.image.load(str(ava_path)).convert_alpha()
    
    @staticmethod
    def load_player_bullet():
        return pg.image.load(BULLET_DIR / "playerbullet.png").convert_alpha()
    
    @staticmethod
    def load_enemy_bullet():
        return pg.image.load(BULLET_DIR / "enemybullet.png").convert_alpha()
        
    
    #TODO: refactor
    # randomised load methods
    # want to randomly select an enemy sprite each time, out of the available enemy files
    # need to use joinpath() here because SPRITE_DIR / returns a WindowsPath object
    # which can't be concatenated properly using +
    @staticmethod
    def load_enemy_ship():
        #count up how many sprites are in the power folder
        sprite_count = len(os.listdir(ENEMY_DIR))
        return pg.image.load(ENEMY_DIR.joinpath("enemy" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()
    
    # loads up a random background image
    @staticmethod
    def load_random_bg():
        #count up how many sprites are in the bg folder
        bg_count = len(os.listdir(BG_DIR))
        return pg.image.load(BG_DIR.joinpath("bg" + str(random.randint(1,bg_count)) + ".png")).convert_alpha()
    
    @staticmethod
    def load_char_bg():
        return pg.image.load(ASSET_DIR / "charsel.png").convert_alpha()

    # load a random power sprite
    @staticmethod
    def load_powerup():
        #count up how many sprites are in the power folder
        sprite_count = len(os.listdir(POWER_DIR))
        return pg.image.load(POWER_DIR.joinpath("power" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()
    
    # font loading
    # loads up the font used for the story crawl
    @staticmethod
    def load_story_font(size):
        font = pg.font.Font(FONT_DIR / "space-wham.ttf", size)
        return font
    