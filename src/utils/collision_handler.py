import pygame as pg

from components.background import Background


class CollisionHandler:
    def __init__(self):
        self.background = Background()
        self.player = None
        self.bullets = pg.sprite.Group() # player bullet group
        self.enemies = pg.sprite.Group() # enemy group
        self.enemy_bullets = pg.sprite.Group() # enemy bullet group
        self.powers = pg.sprite.Group()
        self.hazards = pg.sprite.Group()
        self.boss = None
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.enemy_bullets)
        self.all_sprites.add(self.powers)
        self.all_sprites.add(self.hazards)

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

    def add_powerup(self, power):
        self.powers.add(power)
        self.all_sprites.add(power)

    def add_obstacle(self, hazard):
        self.hazards.append(hazard)
        self.all_sprites.add(hazard)

    def handle_collisions(self):
        # Handle collisions between bullets and enemies
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.collides_with(enemy):
                    bullet.on_collision(enemy)
                    enemy.on_collision(bullet)

        # Handle collisions between enemy bullets and the player
        for bullet in self.enemy_bullets:
            if bullet.collides_with(self.player):
                bullet.on_collision(self.player)
                self.player.on_collision(bullet)

        # Handle collisions between the player and obstacles
        for obstacle in self.obstacles:
            if self.player.collides_with(obstacle):
                self.player.on_collision(obstacle)
                obstacle.on_collision(self.player)

        # Handle collisions between the player and powerups
        for powerup in self.powerups:
            if self.player.collides_with(powerup):
                self.player.on_collision(powerup)
                powerup.on_collision(self.player)

        # Handle collisions between the player and the boss
        if self.boss is not None:
            if self.player.collides_with(self.boss):
                self.player.on_collision(self.boss)
                self.boss.on_collision(self.player)

    def update_physics(self):
        # Update physics for all game objects
        pass
