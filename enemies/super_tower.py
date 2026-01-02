import pygame
import random
import math
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from base.bombs import Bombs, Bomb
from base.boxes import Upgrader, Upgraders


class SuperTower:
    STATE_INIT = 0
    STATE_SHOOT_RANDOM = 1
    STATE_SHOOT_LASER = 2

    def __init__(self, context: PygameContext, dif):
        self.health = 200 + (dif * 50)
        self.x = 465
        self.y = -350
        self.live = False
        self.form = None
        self.state = SuperTower.STATE_INIT
        self.shoot_time = 0
        self.shoot_time_end = 5
        self.shoot_state_end = 0
        self.laser_live = False
        self.laser_end_position = 0
        self.laser_degrees = 90
        self.laser_form = None
        self.circle_r = math.sqrt(((context.width / 2) ** 2) + ((context.height / 2) ** 2))
        self.laser_direction = 1
        self.attack = 60

    def draw(self, context: PygameContext):
        if self.live:
            self.form = pygame.draw.rect(context.screen, (255, 255, 0), (self.x, self.y, 350, 350))

            if self.laser_live:
                self.laser_form = pygame.draw.line(context.screen, (0, 0, 255), (self.x + 175, self.y + 175), self.laser_end_position, 10)

    def control(self, bullets: Bullets, context: PygameContext, upgrades: Upgraders):
        if self.live:
            if self.state == SuperTower.STATE_INIT:
                self.y = self.y + 2.5
                if self.y >= 185:
                    self.state = 1
            else:
                self.shoot_bullets(bullets)
            if self.state == SuperTower.STATE_SHOOT_RANDOM:
                self.shoot_time_end = 3
                self.shoot_state_end = self.shoot_state_end + 1
                if self.shoot_state_end >= 600:
                    self.state = 2
                    self.shoot_time_end = 5
                    self.shoot_state_end = 0
                    self.laser_live = True
                    self.laser_direction = random.randint(0, 1)
                    if self.laser_direction == 0:
                        self.laser_direction = -1
            if self.state == SuperTower.STATE_SHOOT_LASER:
                self.laser_end_position = (context.width / 2 + self.circle_r * math.cos(math.radians(self.laser_degrees)), context.height / 2 + self.circle_r * math.sin(math.radians(self.laser_degrees)))
                self.laser_degrees = self.laser_degrees + (0.5 * self.laser_direction)
                if self.laser_degrees >= 450 or self.laser_degrees <= -270:
                    self.state = 1
                    self.laser_degrees = 90
                    self.laser_live = False

            if self.health <= 0:
                chance = random.randint(1, 10)
                if chance >= 5:
                    upgrades.elements.append(Upgrader(self.x + 150, self.y, 3))
                else:
                    upgrades.elements.append(Upgrader(self.x + 150, self.y, 4))
                self.live = False

    def shoot_bullets(self, bullets: Bullets):
        self.shoot_time = self.shoot_time + 1
        if self.shoot_time >= self.shoot_time_end:
            self.shoot_time = 0
            plus_x = random.randint(-100, 100)
            if plus_x == 0:
                plus_x = plus_x + 1
            plus_x = (self.x + 175) + plus_x
            plus_y = (self.y + 175) + random.randint(-100, 100)
            bullets.elements.append(Bullet(self.x + 175, self.y + 175, plus_x, plus_y, "enemy", 400))

    def contacts(self, bullets: Bullets, player: Player, bombs: Bombs):
        if self.live:
            for bullet in bullets.elements:
                if self.form.colliderect(bullet.form) and bullet.attacker == "friend":
                    self.health = self.health - 1
                    bullet.sharp = False

            for bomb in bombs.elements:
                if self.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_EXPLOSION:
                    bomb.sharp = False
                    self.health = self.health - 10
                if self.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_MOVE:
                    bomb.state = Bomb.STATE_EXPLOSION

            self.attack = self.attack + 1
            if self.form.colliderect(player.r) and self.attack >= 60:
                if player.ship_power == 2:
                    shield = random.randint(0, 100)
                    if shield <= 5:
                        player.health = player.health + 1
                player.health = player.health - 1
                self.attack = 0
            if self.laser_live:
                if self.laser_form.colliderect(player.r) and self.attack >= 60:
                    if player.ship_power == 2:
                        shield = random.randint(0, 100)
                        if shield <= 5:
                            player.health = player.health + 1
                    player.health = player.health - 1
                    self.attack = 0

    def spawn(self):
        self.live = True
