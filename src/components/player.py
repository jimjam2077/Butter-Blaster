import pygame

# passing Sprite makes Player Class a child of Sprite
# can then use super().__init__() to call the Sprite's init() function
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load() #add image here
        self.rect = self.image.get_rect() #defines the borders according to image size
        self.rect.center = () #defines a starting position for rect
        
    
    def update(self):
        
    def draw(self, screen):
        #can add other things to draw here
        screen.blit(self.image, self.rect)
        
    def reset(self):
        