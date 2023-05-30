import os
import random
import pygame as pg
from pathlib import Path
import glob

ROOT_DIR = Path(__file__).parent.parent.parent
ASSET_DIR = ROOT_DIR / "assets"
#under assets
SFX_DIR = ASSET_DIR / "sfx"
MUSIC_DIR = ASSET_DIR / "music"
BG_DIR = ASSET_DIR / "bg"
BULLET_DIR = ASSET_DIR / "bullets"
HAZARD_DIR = ASSET_DIR / "hazards"
TURRET_DIR = ASSET_DIR / "turrets"
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



# Update - originally, it was fine to load and unload assets as needed as I was developing for PC.
# however, in order to create browser-runnable code using pygbag, there needs to be a front-load of most of the
# assets to reduce lag and audio issues. The tradeoff here is higher memory usage, but a smoother
# experience. As this is a small game, it should be ok.
# This problem came up because one of the people that wants to play the game has a Mac, and the python
# code can't be easily cross-compiled for Mac outside of XCode.
class AssetLoader:
    # graphics dictionaries - in most cases the inner dictionaries of each dictionary
    # contain lists of loaded image assets
    bullets = { #bullets["bullets"] will have ["dune", "toad", "assist",...]
        "bullets": {},
        "boss_bullets": {},
        "turret_bullets": {}
    }
    
    backgrounds = {
        "screens": {},
        "level": {},
        "boss": {}
    }
    
    animations = { # contains lists of sprite animations, should be sorted
        "dune": {},
        "toad": {},
        "eye": {},
        "mouth": {},
        "spider": {},
        "explosion": {},
    }
    
    entities = {
        "enemy_ships": {},
        "npcs": {},
        "powers": {},
        "turrets": {},
        "hazards": {}
    }
    
    ui_parts = {
        "portraits": {},
        "nameplates": {},
    }
    
    fonts = {
        "main_menu": None,
        "story": None,
        "end_screen": None,
        "ui": None
    }
    
    # sounds and music
    sfx = {}
    music = {}
    
    @staticmethod
    def load_assets():
        AssetLoader.load_bullets()
        AssetLoader.load_backgrounds()
        AssetLoader.load_animations()
        AssetLoader.load_entities()
        AssetLoader.load_ui_elements()
        AssetLoader.load_fonts()
        AssetLoader.load_sfx()
        AssetLoader.load_music()
       
    @staticmethod # new method
    def load_bullets(): 
        AssetLoader.bullets = {
            "bullets": {
                "toad": pg.image.load(str(BULLET_DIR / "toadbullet.png")).convert_alpha(),
                "dune": pg.image.load(str(BULLET_DIR / "dunebullet.png")).convert_alpha(),
                "enemy": pg.image.load(str(BULLET_DIR / "enemybullet.png")).convert_alpha(),
                "ally": pg.image.load(str(BULLET_DIR / "allybullet.png")).convert_alpha(),
                "spider": pg.image.load(str(BULLET_DIR / "spider.png")).convert_alpha(),
                "chip": pg.image.load(str(BULLET_DIR / "dorito.png")).convert_alpha()
            },
            "boss_bullets": AssetLoader.load_images_with_prefix(BULLET_DIR, "baby"),
            "turret_bullets": AssetLoader.load_images_with_prefix(BULLET_DIR, "bit")
        }
    
    @staticmethod # new method
    def load_entities():
        AssetLoader.entities = {
            "enemy_ships": AssetLoader.load_images_with_prefix(ENEMY_DIR, "enemy"),
            "npcs": {
                "jena": pg.image.load(str(SPRITE_DIR / "jena.png")).convert_alpha(),
                "boss": pg.image.load(str(BOSS_DIR / "idle1.png")).convert_alpha()
            },
            "powers": AssetLoader.load_images_with_prefix(POWER_DIR, "power"),
            "turrets": AssetLoader.load_images_with_prefix(TURRET_DIR, "turret"),
            "hazards": AssetLoader.load_images_with_prefix(HAZARD_DIR, "hazard")
        }
    
    @staticmethod # new method
    def load_backgrounds():
        AssetLoader.backgrounds = {
            "screens":{
                "title": pg.image.load(str(ASSET_DIR / "title.png")).convert(),
                "charsel": pg.image.load(str(ASSET_DIR / "charsel.png")).convert(),  
            },
            "level": AssetLoader.load_images_with_prefix(BG_DIR / "level", "bg"),
            "boss": AssetLoader.load_images_with_prefix(BG_DIR / "boss", "bg")
        }
                
    @staticmethod # new method
    def load_animations():
        AssetLoader.animations = {
            "dune": AssetLoader.load_images_with_prefix(DUNE_DIR, "duneship"),
            "toad": AssetLoader.load_images_with_prefix(TOAD_DIR, "toadship"),
            "eye": AssetLoader.load_images_with_prefix(BOSS_DIR / "eye", "eye"),
            "mouth": AssetLoader.load_images_with_prefix(BOSS_DIR / "mouth", "mouth"),
            "spider": AssetLoader.load_images_with_prefix(BOSS_DIR / "spider", "spider"),
            "explosion": AssetLoader.load_images_with_prefix(EXPLO_DIR, "explode")
        }
    
    @staticmethod # new method - maybe move all UI things to a UI class
    def load_ui_elements():
        AssetLoader.ui_parts = {
            "portraits":{
                "dune": pg.image.load(str(UI_DIR / "dune.png")).convert_alpha(),
                "toad": pg.image.load(str(UI_DIR / "toad.png")).convert_alpha(),
                "andy": pg.image.load(str(UI_DIR / "andy.png")).convert_alpha(),
                "wes": pg.image.load(str(UI_DIR / "wes.png")).convert_alpha(),
                "jena": pg.image.load(str(UI_DIR / "jena.png")).convert_alpha()
            },
            "nameplates":{
                "dune": pg.image.load(str(UI_DIR / "dunetxt.png")).convert_alpha(),
                "toad": pg.image.load(str(UI_DIR / "toadtxt.png")).convert_alpha(),
                "jena": pg.image.load(str(UI_DIR / "jenatxt.png")).convert_alpha(),
            }
        }
    
    @staticmethod # new method
    def get_icon():
        icon = pg.image.load(str(ASSET_DIR / "icon.png")).convert_alpha()
        return icon
        
    @staticmethod # new method
    def load_fonts():
        """ loads up all of the game's used fonts at the specified sized.
        """
        AssetLoader.fonts["instruction"] = pg.font.Font(FONT_DIR / "space-wham.ttf", 34)
        AssetLoader.fonts["story"] = pg.font.Font(FONT_DIR / "space-wham.ttf", 35)
        AssetLoader.fonts["flavour"] = pg.font.Font(FONT_DIR / "space-wham.ttf", 26)
        AssetLoader.fonts["ui"] = pg.font.Font(FONT_DIR / "space-wham.ttf", 11)
                

    @staticmethod # new method
    def load_images_with_prefix(dir, prefix):
        """ returns a sorted dictionary of loaded images from the specified directory. 
            assumes that image sets use a naming convention of <prefix><number>
        
        Args:
            prefix (String): the folder the images are expected to be in
            prefix (String): the name used as the prefix for a file which may 
                             have multiple numbered versions

        Returns:
            dict: A dictionary mapping filenames (without the extension) to loaded images.
        """
        imgs = {}
        file_pattern = str(dir / f"{prefix}*.png")
        file_paths = glob.glob(file_pattern)  # Get the file paths
        file_paths.sort(key=lambda path: int(Path(path).stem[len(prefix):]))
        for file_path in file_paths:
            filename = Path(file_path).stem
            if "bg" in filename:
                img = pg.image.load(file_path).convert_alpha()
            else:
                img = pg.image.load(file_path).convert_alpha()
            imgs[filename] = img
        return imgs

    @staticmethod
    def get_random_power():
        num = str(random.choices(range(1, 4), WEIGHTS)[0])
        power_image = AssetLoader.entities["powers"]["power" + num]
        power_name = POWERS[num]
        return power_image, power_name

    @staticmethod
    def load_sfx():
        """Load sound effects from the specified directory and store them in the `sfx` dictionary.
        The sound files are expected to be located in the directory specified by `SFX_DIR`.
        Each sound file is loaded using `pg.mixer.Sound` and stored in the `sfx` dictionary,
        with the filename stem as the key and the loaded sound as the value.
        """
        for file_name in os.listdir(str(SFX_DIR)):
            file_path = os.path.join(str(SFX_DIR), file_name)
            if os.path.isfile(file_path):
                sound_name = os.path.splitext(file_name)[0]
                sound = pg.mixer.Sound(file_path)
                if "shoot" in sound_name:
                    sound.set_volume(0.1)
                elif "meow" in sound_name:
                    sound.set_volume(1.0)
                else:
                    sound.set_volume(0.25)
                AssetLoader.sfx[sound_name] = sound
    
    @staticmethod
    def load_music():
        """Load sound effects from the specified directory and store them in the `sfx` dictionary.
        The sound files are expected to be located in the directory specified by `SFX_DIR`.
        Each sound file is loaded using `pg.mixer.Sound` and stored in the `sfx` dictionary,
        with the filename stem as the key and the loaded sound as the value.
        """
        for file_name in os.listdir(str(MUSIC_DIR)):
            file_path = os.path.join(str(MUSIC_DIR), file_name)
            if os.path.isfile(file_path):
                song_name = os.path.splitext(file_name)[0]
                song = pg.mixer.Sound(file_path)
                if "military" in song_name:
                    song.set_volume(0.08)
                elif "story" in song_name:
                    song.set_volume(0.5)
                else:
                    song.set_volume(0.2)
                AssetLoader.music[song_name] = song

    @staticmethod
    def play_bgm(song_type):
        # Get all songs of the specified song_type
        songs = [key for key in AssetLoader.music.keys() if key.startswith(song_type)]
        if songs:
            random_song = random.choice(songs)
            
            # Check if any sound is already playing
            # Check if the chosen sound or any other sound is already playing
            if any(AssetLoader.music[song].get_num_channels() > 0 for song in songs):
                return
            # Play the selected song
            AssetLoader.music[random_song].play()

    #### old methods ####
    @staticmethod
    def load_boss_bullets():
        boss_bullets = {}
        for i in range(1, 11):
            filename = f"baby{i}.png"
            bullet_image = pg.image.load(str(BULLET_DIR / filename)).convert_alpha()
            boss_bullets[f"baby{i}"] = bullet_image
        return boss_bullets
    
        
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
    def load_sprite_list(sub_folder):
        """Loads up a set of sprites to use in an animation, in order.
           Assumes a naming convention using a number at the end of each file

        Args:
            dir (String): the name of the folder to look in

        Returns:
            List: a list of images representing an animation for a sprite
        """
        images = []
        dir_path = os.path.join(SPRITE_DIR, sub_folder)
        file_names = [f for f in os.listdir(dir_path) if f.endswith('.png') or f.endswith('.jpg')]
        file_names = sorted(file_names, key=lambda x: int(x[-5]))

        for file_name in file_names:
            image_path = os.path.join(dir_path, file_name)
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
    def load_turret():
        sprite_count = len(os.listdir(TURRET_DIR))
        return pg.image.load(TURRET_DIR.joinpath("turret" + str(random.randint(1,sprite_count)) + ".png")).convert_alpha()
    
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
    def load_random_bg(sub_folder):
        dir_path = os.path.join(BG_DIR, sub_folder)
        #count up how many sprites are in the bg folder
        bg_count = len(os.listdir(BG_DIR))
        return pg.image.load(os.path.join(dir_path, "bg" + str(random.randint(1, bg_count)) + ".png")).convert_alpha()

    
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
    