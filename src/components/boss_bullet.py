import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos):
        super().__init__()
        
        self.rect = self.image.get_rect(center=pos)  # set the initial position of the bullet
        self.target_pos = target_pos  # store the target position
        self.speed = 200  # set the speed of the bullet

    def update(self, dt):
        # move towards the target position
        if self.rect.x > self.target_pos[0]:
            self.rect.x -= self.speed *dt
        if self.rect.y > self.target_pos[1]:
            self.rect.y -= self.speed *dt
        elif self.rect.y < self.target_pos[1]:
            self.rect.y += self.speed *dt

    def draw(self, screen):
        # can add other things to draw here
        screen.blit(self.image, self.rect)