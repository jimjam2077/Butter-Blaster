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
BOSS_DIR = SPRITE_DIR / "boss"

POWERS = {
    '1': "pill",
    '2': "taser",
    '3': "assist"
}
WEIGHTS = [60, 25, 15] # adjust to decide how often 1, 2 or 3 is chosen

# this could be a bunch of static variables
# i.e. PLAYER_SHIP = pygame.image.load(file).convert_alpha()
# however, it would mean more memory overhead as everything is loaded at once
# doing it this way means assets are loaded as they are needed
# not really a big concern because this is a tiny game
class AssetLoader:
    
    # loads a set of player ship sprites from a named folder
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
    
    @staticmethod # this should really use a sprite sheet instead, but it'll do for now!
    def load_sprite_list(dir):
        """Loads up a set of sprites to use in an animation, in order.
           Assumes a naming convention using a number at the end of each file

        Args:
            dir (String): the name of the folder to look in

        Returns:
            List: a list of images representing an animation for a sprite
        """
        images = []
        directory_path = os.path.join(SPRITE_DIR, dir)
        file_names = [f for f in os.listdir(directory_path) if f.endswith('.png') or f.endswith('.jpg')]
        file_names = sorted(file_names, key=lambda x: int(x[-5]))

        for file_name in file_names:
            image_path = os.path.join(directory_path, file_name)
            image = pg.image.load(image_path).convert_alpha()
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
    def load_jena():
        return pg.image.load(SPRITE_DIR / "jena.png").convert_alpha()
    
    @staticmethod
    def load_boss_img():
        return pg.image.load(BOSS_DIR / "idle1.png")
    
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
    
    @staticmethod
    def load_bullet(file):
        return pg.image.load(BULLET_DIR / file).convert_alpha()  
    
    #TODO: Load_enemy, load_background, load_hazard and load power are all similar and could be one method
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

    @staticmethod
    def load_hazard():
        sprite_count = len(os.listdir(HAZARD_DIR))
        return pg.image.load(HAZARD_DIR.joinpath("hazard" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()

    # load a random power sprite
    @staticmethod
    def load_powerup():
        #count up how many sprites are in the power folder
        num = str(random.choices(range(1, 4), WEIGHTS)[0])
        return pg.image.load(POWER_DIR.joinpath("power" + num + ".png")).convert_alpha(), POWERS[num]
    
    # font loading
    # loads up the font used for the story crawl
    @staticmethod
    def load_story_font(size):
        font = pg.font.Font(FONT_DIR / "space-wham.ttf", size)
        return font
    