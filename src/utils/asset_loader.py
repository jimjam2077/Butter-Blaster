import random
import pygame as pg
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
ASSET_DIR = ROOT_DIR / "assets"
BULLET_DIR = ASSET_DIR / "bullets"
SPRITE_DIR = ASSET_DIR / "sprites"
UI_DIR = ASSET_DIR / "ui"

# this could be a bunch of static variables
# i.e. PLAYER_SHIP = pygame.image.load(file).convert_alpha()
# however, it would mean more memory overhead as everything is loaded at once
# doing it this way means assets are loaded as they are needed
# not really a big concern because this is a tiny game
class AssetLoader:
    
    @staticmethod
    def load_toad_ship():
        return pg.image.load(SPRITE_DIR / "toadship.png").convert_alpha()
    
    @staticmethod #change this
    def load_dune_ship():
        return pg.image.load(SPRITE_DIR / "toadship.png").convert_alpha()
    
    # want to randomly select an enemy sprite each time, out of the available enemy files
    # need to use joinpath() here because SPRITE_DIR / returns a WindowsPath object
    # which can't be concatenated properly using +
    @staticmethod
    def load_enemy_ship():
        return pg.image.load(SPRITE_DIR.joinpath("enemy" + str(random.randint(1,4)) + ".png")).convert_alpha()
    
    @staticmethod
    def load_player_bullet():
        return pg.image.load(BULLET_DIR / "playerbullet.png").convert_alpha()
    
    @staticmethod
    def load_enemy_bullet():
        return pg.image.load(BULLET_DIR / "enemybullet.png").convert_alpha()
    
    