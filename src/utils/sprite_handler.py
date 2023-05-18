import math
import random
import pygame as pg
from components.background import Background
from components.boss import Boss
from components.enemy import Enemy
from components.jena import Jena
from config import Config
from components.explosion import Explosion
from components.power import Power
from utils.audio_loader import AudioLoader


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
        if self.boss is not None:
            self.background.fade_boss_bg(delta_time)
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
        self.detect_player_collision()
        self.detect_enemy_collision()
        self.detect_power_collision()
        self.detect_hazard_collision()
        if self.boss is not None:
            self.detect_boss_collision()
        
    
    def detect_player_collision(self):
        """ Looks for collisions between the player and all types of external entities,
            such as enemies and their bullets, hazard, and bosses
        """
        now = pg.time.get_ticks()
        if now - self.player.last_hit_time <= Config.INVULN_WINDOW:
            return
        collision_data = { # use this dictionary to specify how much damage each type of collision should do
        'bullet': {'damage': 1},
        'hazard': {'damage': 2, 'bounce': True},
        'ship': {'damage': 2},
        'boss': {'damage': 4}
        }
        
        collisions = { # use this dictionary to retrieve results for each type of collidable object
            'bullet': pg.sprite.spritecollide(self.player, self.enemy_bullets, True, pg.sprite.collide_mask),
            'hazard': pg.sprite.spritecollide(self.player, self.hazards, False, pg.sprite.collide_mask),
            'ship': pg.sprite.spritecollide(self.player, self.enemies, True),
            'boss': pg.sprite.collide_mask(self.player, self.boss) if self.boss else []
        }
        
        for collision_type, collision_result in collisions.items():
            if collision_result:
                self.player.add_damage(collision_data[collision_type]['damage'])
                explosion = Explosion(self.player.rect.center, 0)
                self.all_sprites.add(explosion)
                AudioLoader.explosion_sound()
                if 'bounce' in collision_data[collision_type]:
                    for hazard in collision_result:
                        dx, dy = self.player.rect.centerx - hazard.rect.centerx, self.player.rect.centery - hazard.rect.centery
                        dist = math.hypot(dx, dy)
                        if dist != 0:
                            self.player.rect.centerx += dx / dist * 15
                            self.player.rect.centery += dy / dist * 15
                self.player.last_hit_time = now

    
    def detect_enemy_collision(self):
        """Looks for collisions between player bullets and enemy rects
        
        Args:
            hazards (pg.Group): the sprite group containing hazards
            all_sprites (pg.Group): the sprite group containing all sprites
            bullets (pg.Group): the sprite group containing player bullets
            enemy_grp (pg.Group): the sprite group containing enemies
            powers (pg.Group): the sprite group containing powers
        """
        # Check for collisions between bullets and enemies
        # Check for collisions between bullets and enemies
        bullet_enemy_collisions = pg.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, enemy_list in bullet_enemy_collisions.items():
            for enemy in enemy_list:
                print("enemy killed")
                # Add power with a 8% chance at the center of the enemy rect
                if random.random() < 0.90:
                    if self.boss is not None:
                        power = Power(enemy.rect.center, 0)
                    else: 
                        power = Power(enemy.rect.center)
                    self.all_sprites.add(power)
                    self.powers.add(power)    
                explosion = Explosion(enemy.rect.center)
                self.all_sprites.add(explosion)
                self.player.increase_score()

    def detect_boss_collision(self):
        hit_by_bullet = pg.sprite.spritecollide(self.boss, self.bullets, True, pg.sprite.collide_mask)
        for bullet in hit_by_bullet:
            self.boss.add_damage(self.player.get_damage())
            explosion = Explosion(bullet.rect.center, 0)
            self.all_sprites.add(explosion)

    def detect_hazard_collision(self):
        # Check for collisions between bullets and hazards
        bullet_hazard_collisions = pg.sprite.groupcollide(self.bullets, self.hazards, True, False, pg.sprite.collide_mask)
        for bullet, hazards_list in bullet_hazard_collisions.items():
            for hazard in hazards_list:
                # Kill bullet if it collides with a hazard
                bullet.kill()
    
    
    def detect_power_collision(self):
        #handle powerups!
        touched_powers = pg.sprite.spritecollide(self.player, self.powers, True)
        for power in touched_powers:
            AudioLoader.pickup_sound()
            if power.get_name() == "assist":
                self.player.add_assist()
            if power.get_name() == "pill":
                self.player.add_health(2)
            if power.get_name() == "taser":
                if self.player.level == 3:
                    self.player.add_health(1)
                elif self.player.level < 3:
                    self.player.damage *= 1.2599210498948732
                    if self.player.level<2:
                        self.player.shot_delay *= 0.5477
                    self.player.increase_level()
            # add other power-up handling logic here

