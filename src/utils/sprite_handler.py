import pygame as pg
from components.background import Background
from components.boss import Boss
from components.enemy import Enemy
from components.jena import Jena


class SpriteHandler:
    def __init__(self):
        self.background = Background()
        self.player = None
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.powers = pg.sprite.Group()
        self.hazards = pg.sprite.Group()
        self.boss = None
        self.clock = None
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)
        self.all_sprites.add(self.powers)
        self.all_sprites.add(self.hazards)
   
    def add_explosion(self, explosion):
        self.all_sprites.add(explosion)
    
    def add_player(self, player):
        self.player = player
        self.player.reset()
        self.all_sprites.add(player)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def add_enemy_bullet(self, bullet):
        self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)

    def add_enemy(self, enemy):
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_boss(self, boss):
        self.boss = boss
        self.all_sprites.add(boss)

    def add_power(self, power):
        self.powers.add(power)
        self.all_sprites.add(power)

    def add_hazard(self, hazard):
        self.hazards.add(hazard)
        self.all_sprites.add(hazard)

    def update_all_sprites(self, delta_time):
        self.background.update(self, delta_time)  
        self.player.update(self, delta_time)
        for sprite in self.all_sprites:
            if sprite != self.player:
                if isinstance(sprite, Enemy):
                    sprite.update(self, delta_time)
                elif isinstance(sprite, Jena) or isinstance(sprite, Boss):
                    sprite.update(self, delta_time)
                else:
                    sprite.update(self, delta_time)
                    
    def check_collisions(self, delta_time):
        pass
    
    def check_player_hit

