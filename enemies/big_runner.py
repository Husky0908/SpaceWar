import pygame
import random
from base.context import PygameContext
from base.directions import get_direction
from base.bullets import Bullet, Bullets
from base.player import Player
from enemies.runners import Runners
from base.boxes import Upgraders, Upgrader


class BigRunner:
    STATE_INIT = 0
    STATE_FAST_MOVE = 1
    STATE_PAUSE = 2

    def __init__(self, context: PygameContext, dif: int):
        self.x = context.width // 2 - 75
        self.y = -210
        self.health = 100 + (dif * 20)
        self.status = 1
        self.form = None
        self.live = False
        self.state = BigRunner.STATE_INIT
        self.x_0 = 0
        self.y_0 = 0
        self.dir_x = 0
        self.dir_y = 0
        self.start_time = 0
        self.how_long = None
        self.speed = 250
        self.dir = 1
        self.shoot_time = 0
        self.shoot_time_end = 60
        self.attack = 0
        self.how_many_run = random.randint(2, 4) * 2
        self.last_point = self.health
        self.damage_status = self.health / 4

    def draw(self, context: PygameContext):
        if self.live:
            self.form = pygame.draw.rect(context.screen, (255, 255, 255), (self.x, self.y, 150, 210))

    def spawn(self):
        self.live = True

    def control(self, context: PygameContext, bullets: Bullets, runners: Runners, upgrades: Upgraders):
        if self.live:
            if self.state == BigRunner.STATE_INIT:
                self.control_init()
                self.control_create_dest(context, runners)
            if self.state == BigRunner.STATE_FAST_MOVE:
                self.control_fast_move(context, bullets, runners)
            if self.state == BigRunner.STATE_PAUSE:
                self.control_pause(context, runners)

            if self.health <= self.last_point - self.damage_status:
                self.last_point = self.last_point - self.damage_status
                self.status = self.status + 1
            if self.health <= 0:
                chance = random.randint(1, 10)
                if chance >= 4:
                    upgrades.elements.append(Upgrader(self.x + 150, self.y, 3))
                else:
                    upgrades.elements.append(Upgrader(self.x + 150, self.y, 2))
                self.live = False

    def control_init(self):
        self.y = self.y + 4
        if self.y >= 0:
            self.state = BigRunner.STATE_FAST_MOVE

    def control_fast_move(self, context: PygameContext, bullets: Bullets, runners: Runners):
        d_t = context.time - self.start_time
        if self.dir == 1:
            self.how_long = (self.y >= 510)
        else:
            self.how_long = (self.y <= 0)
        if not self.how_long:
            self.x = self.x_0 + self.dir_x * d_t * self.speed
            self.y = self.y_0 + self.dir_y * d_t * self.speed
            self.control_shoot_bullets(bullets)
        else:
            self.start_time = context.time
            if self.dir == 1:
                self.dir = 2
            else:
                self.dir = 1
            self.control_create_dest(context, runners)

    def control_create_dest(self, context: PygameContext, runners: Runners):
        if not self.state == BigRunner.STATE_INIT:
            self.how_many_run = self.how_many_run - 1
        if self.how_many_run <= 0:
            self.state = BigRunner.STATE_PAUSE
            for i in range(self.status - 1):
                runners.spawn(context)
        if self.dir == 1:
            dest_x, dest_y = (random.randint(0, 1130), 720)
        else:
            dest_x, dest_y = (random.randint(0, 1130), 0)
        self.dir_x, self.dir_y = get_direction(self.x, self.y, dest_x, dest_y)
        self.start_time = context.time
        self.x_0, self.y_0 = self.x, self.y

    def control_shoot_bullets(self, bullets: Bullets):
        self.shoot_time = self.shoot_time + 1
        if self.shoot_time >= self.shoot_time_end:
            self.shoot_time = 0
            bullets.elements.append(Bullet(self.x, self.y + 105, self.x - 1, self.y + 105, "enemy"))
            bullets.elements.append(Bullet(self.x + 150, self.y + 105, self.x + 151, self.y + 105, "enemy"))

    def contacts(self, player: Player, bullets: Bullets):
        if self.live:
            if self.form.colliderect(player.form) and self.attack >= 60:
                if player.ship_power == 2:
                    shield = random.randint(0, 100)
                    if shield <= 5:
                        player.health = player.health + 1
                player.health = player.health - 1
                self.attack = 0
            self.attack = self.attack + 1

            for bullet in bullets.elements:
                if bullet.form.colliderect(self.form) and bullet.attacker == "friend":
                    self.health = self.health - 1
                    bullet.sharp = False

    def control_pause(self, context: PygameContext, runners: Runners):
        if context.time - self.start_time >= 3:
            self.how_many_run = random.randint(2, 4) * 2 - 1
            self.control_create_dest(context, runners)
            self.state = BigRunner.STATE_FAST_MOVE
        if self.status == 2:
            self.speed = 325
            self.shoot_time_end = 50
        if self.status == 3:
            self.speed = 400
            self.shoot_time_end = 40
        if self.status == 4:
            self.speed = 500
            self.shoot_time_end = 30
