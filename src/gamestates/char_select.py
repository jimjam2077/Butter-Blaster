import sys
from gamestates.state import State
from config import Config
from gamestates.story_scroll import StoryScroll
from utils.audio_loader import AudioLoader
from utils.asset_loader import AssetLoader
import pygame as pg

class CharSelect(State):
    def __init__(self, game):
        super().__init__(game)
        self._faded_in = False
        self._fade_spd = 255 / (2 * 60)  # 2 seconds at 60fps
        self._alpha = 0

        # Load images
        self._toad_img = AssetLoader.load_avatar("toad")
        self._dune_img = AssetLoader.load_avatar("dune")
        self._jena_img = AssetLoader.load_avatar("jena")

        # Create image rects
        center = (Config.WIDTH / 2, Config.HEIGHT / 2)
        self._toad_rect = self._toad_img.get_rect(center=center)
        self._toad_orig = self._toad_rect
        self._dune_rect = self._dune_img.get_rect(center=center).move(-300, 0)
        self._dune_orig = self._dune_rect
        self._jena_rect = self._jena_img.get_rect(center=center).move(300, 0)
        self._jena_orig_size = self._jena_rect.size

        # Create title text
        self._title_font = AssetLoader.load_story_font(64)
        self._title_text = self._title_font.render("SELECT YOUR PILOT", True, pg.Color("firebrick2"))
        self._title_rect = self._title_text.get_rect(center=center).move(0, -250)

        # Create nameplates
        self._dune_name = AssetLoader.load_nameplate("dune")
        self._toad_name = AssetLoader.load_nameplate("toad")
        self._jena_name = AssetLoader.load_nameplate("jena")
        self._d_n_rect = self._dune_name.get_rect(center=self._dune_rect.center).move(0, 150)
        self._t_n_rect = self._toad_name.get_rect(center=self._toad_rect.center).move(0, 150)
        self._j_n_rect = self._jena_name.get_rect(center=self._jena_rect.center).move(0, 150)

        # Create background 
        self._bg = AssetLoader.load_char_bg()
        self._bg_rect = self._bg.get_rect(center=center)

        # Create characters dictionary
        self._characters = {
            "toad": self._toad_rect,
            "dune": self._dune_rect
        }

        # Set up image scaling variables
        self._toad_scaled = False
        self._dune_scaled = False

        # Set up surfaces with zero alpha
        self._surfaces = [
            self._bg, self._toad_img, self._dune_img, self._jena_img,
            self._title_text, self._dune_name, self._toad_name, self._jena_name
        ]
        for surface in self._surfaces:
            surface.set_alpha(0)

        
    def update(self, delta_time):
        # potentially another way to do this - cover the screen
        # with a black surface and slowly reduce its alpha
        # should be fast regardless, so leaving it for now
        if not self._faded_in: 
            for s in self._surfaces:
                self.fade_in(delta_time, s, "_faded_in")
        AudioLoader.play_menu_music()
           
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # iterate over characters dictionary to check if a rectangle has been clicked
                for char_name, char_rect in self._characters.items():
                    if char_rect.collidepoint(pg.mouse.get_pos()):
                        AudioLoader.stop_sound()
                        self.game.set_pilot(char_name)
                        new_state = StoryScroll(self.game)
                        new_state.enter_state()
                        break #exit the loop
        #print(self._toad_rect.width)
        self._toad_img, self._toad_rect = self.check_mouseover(self._toad_img, self._toad_rect, "toad")
        self._dune_img, self._dune_rect = self.check_mouseover(self._dune_img, self._dune_rect, "dune")

    def check_mouseover(self, img, rect, name):
        """Checks whether the mouse is positioned inside the provided rect
            if it is, the image and rect are transformed
            if it's not, the image and rect are reloaded 
        Args:
            img (pygame.Surface): the image to be processed
            rect (pygame.Rect): a rect to use for mouse collision
            name (String): the name of the avatar that needs to be reloaded

        Returns:
            _type_: _description_
        """
        if rect.collidepoint(pg.mouse.get_pos()):
            if rect.width == 200: # check for original size
                img, rect = self.scale_on_mouseover(img, rect)
        else: # reload the image to original size
            img, rect = AssetLoader.load_avatar(name), img.get_rect(center=rect.center)
        return img, rect
 

    def render(self, display):
        """Render step called by the game's main loop to update the given display

        Args:
            display (pygame.Surface): The surface to which the game is rendered.
        """
        #start drawing. draw base elements at the top
        display.fill((0,0,0)) # fill screen
        display.blit(self._bg, self._bg_rect) # draw the background
        display.blit(self._title_text, self._title_rect) # draw title
        display.blit(self._dune_img, self._dune_rect) # draw the portraits
        display.blit(self._toad_img, self._toad_rect)
        display.blit(self._jena_img, self._jena_rect)
        display.blit(self._dune_name, self._d_n_rect) #draw the text relative to the images
        display.blit(self._toad_name, self._t_n_rect)
        display.blit(self._jena_name, self._j_n_rect)
        pg.display.update()
    
    
    def scale_on_mouseover(self, image, rect):
        """Performs scale transformation on a pygame image
            and returns the scaled image along with a new rectangle

        Args:
            image (pygame.Surface): surface representing an image to be scaled up
            rect (pygame.Rect): a pygame rect object associated with the image

        Returns:
            _type_: _description_
        """
        # Calculate the new size for the image
        new_size = (int(rect.width * 1.1), int(rect.height * 1.1))
        # Scale the image
        scaled_image = pg.transform.scale(image, new_size)
        # Calculate the new rect with the same center as the original rect
        new_rect = scaled_image.get_rect(center=rect.center)
        # Return the scaled image and rect
        return scaled_image, new_rect
  
    
    def fade_in(self, delta_time, surface, faded_variable_name):
        """takes a given surface and increases the alpha until it is visible

        Args:
            delta_time (float): amount of time between render frames
            surface (pygame.Surface): a pygame surface to fade in
            faded_variable_name (bool): the boolean to be set once the surface is visible
        """        
        faded_variable = getattr(self, faded_variable_name)
        self._alpha += self._fade_spd * delta_time * 60
        if self._alpha >= 255:
            self._alpha = 255
            setattr(self, faded_variable_name, not faded_variable)
        surface.set_alpha(int(self._alpha))
       
        
"""   
        if self._toad_rect.collidepoint(pg.mouse.get_pos()):
            if self._toad_rect.width == 200: # toad not scaled yet
                # Scale image by 10%
                self._toad_img, self._toad_rect = self.scale_on_mouseover(self._toad_img, self._toad_rect)
        else:
            # Reset image to original size
            self._toad_img, self._toad_rect = AssetLoader.load_avatar("toad"), self._toad_img.get_rect(center=self._toad_orig.center)
"""
        
        
"""    def check_mouse_hover(self):
        if self._toad_rect.collidepoint(pg.mouse.get_pos()):
            if not self._toad_scaled: # toad not scaled yet
                # Scale image by 10%
                self._toad_img, self._toad_rect = self.scale_on_mouseover(self._toad_img, self._toad_rect)
                self._toad_scaled = True
        else:
            # Reset image to original size
            self._toad_img, self._toad_rect = AssetLoader.load_avatar("toad"), self._toad_img.get_rect(center=self._toad_rect.center)
            self._toad_scaled = False
"""