import pygame
import random
from base.context import PygameContext
from base.directions import get_direction, get_delta_vector
from base.bullets import Bullets, Bullet
from base.player import Player


class HeavyGunner:
    STATE_INIT = 0
    STATE_WHERE_MOVE = 1
    STATE_MOVE = 2
    STATE_SHOOT = 3

    def __init__(self):
        self.x = random.randint(100, 1000)
        self.y = -100
        self.form = None
        self.state = HeavyGunner.STATE_INIT
        self.moving = 0
        self.dest_x = 0
        self.dest_y = 0
        self.start_time = 0
        self.x_0 = self.x
        self.y_0 = self.y
        self.dir_x = 0
        self.dir_y = 0
        self.time = 0
        self.speed = 160
        self.player_x = 0
        self.player_y = 0
        self.asteroid = False
        self.shoot = 0

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (0, 0, 255), (self.x, self.y, 75, 75))

    def control(self, context: PygameContext, bullets: Bullets, player: Player):
        if self.state == HeavyGunner.STATE_INIT:
            self.y = self.y + 2
            if self.y >= 25:
                self.state = HeavyGunner.STATE_WHERE_MOVE
                self.moving = random.randint(2, 3)
        if self.state == HeavyGunner.STATE_WHERE_MOVE:
            self.dest_x = random.randint(75, context.width - 75)
            self.dest_y = random.randint(0 + 75, context.height - 75)
            self.start_time = context.time
            self.x_0, self.y_0 = self.x, self.y
            self.dir_x, self.dir_y = get_direction(self.x_0, self.y_0, self.dest_x, self.dest_y)
            self.time = random.randint(1, 3)
            self.state = HeavyGunner.STATE_MOVE
        if self.state == HeavyGunner.STATE_MOVE:
            d_t = context.time - self.start_time
            if d_t < self.time:
                self.x = self.x_0 + self.dir_x * d_t * self.speed
                self.y = self.y_0 + self.dir_y * d_t * self.speed
            else:
                self.moving = self.moving - 1
                if not self.moving == 0:
                    self.state = HeavyGunner.STATE_WHERE_MOVE
                else:
                    self.state = HeavyGunner.STATE_SHOOT
                    self.player_x = player.x
                    self.player_y = player.y
                    self.shoot = 1
        if self.state == HeavyGunner.STATE_SHOOT:
            delta_x, delta_y = get_delta_vector(self.x, self.y, self.player_x, self.player_y)

            if delta_x == 0:
                delta_x = delta_x + 0.1

            tg_alfa = delta_y / delta_x

            if self.shoot == 1 or self.shoot == 5:
                plus_sign = 1
                if tg_alfa < -1.73205:
                    plus_sign = -1

                minus_sign = 1
                if tg_alfa > 1.73205:
                    minus_sign = -1

                new_1_x = self.x + minus_sign * delta_x
                new_1_y = self.y + minus_sign * (delta_y + 0.5773 * delta_x) / (1 - (delta_y/delta_x * 0.5773))
                new_2_x = self.x + plus_sign * delta_x
                new_2_y = self.y + plus_sign * (delta_y - 0.5773 * delta_x) / (1 + (delta_y/delta_x * 0.5773))

                bullets.elements.append(Bullet(self.x, self.y, self.player_x, self.player_y, "enemy"))
                bullets.elements.append(Bullet(self.x, self.y, new_1_x, new_1_y, "enemy"))
                bullets.elements.append(Bullet(self.x, self.y, new_2_x, new_2_y, "enemy"))

                self.shoot = self.shoot + 1
                self.start_time = context.time

            if self.shoot == 3:
                plus_sign = 1
                if tg_alfa < -3.73205:
                    plus_sign = -1

                minus_sign = 1
                if tg_alfa > 3.73205:
                    minus_sign = -1

                new_1_x = self.x + minus_sign * delta_x
                new_1_y = self.y + minus_sign * (delta_y + 0.2679 * delta_x) / (1 - (delta_y/delta_x * 0.2679))
                new_2_x = self.x + plus_sign * delta_x
                new_2_y = self.y + plus_sign * (delta_y - 0.2679 * delta_x) / (1 + (delta_y/delta_x * 0.2679))

                bullets.elements.append(Bullet(self.x, self.y, new_1_x, new_1_y, "enemy"))
                bullets.elements.append(Bullet(self.x, self.y, new_2_x, new_2_y, "enemy"))

                self.shoot = self.shoot + 1
                self.start_time = context.time

            if (self.shoot == 2 or self.shoot == 4) and context.time - self.start_time >= 0.5:
                self.shoot = self.shoot + 1

            if self.shoot == 6:
                self.state = HeavyGunner.STATE_WHERE_MOVE
                self.moving = random.randint(2, 3)


class HeavyGunners:
    def __init__(self):
        self.elements = []

    def spawn(self):
        self.elements.append(HeavyGunner())

    def draw(self, context: PygameContext):
        for heavy_gunner in self.elements:
            heavy_gunner.draw(context)

    def control(self, context: PygameContext, bullets: Bullets, player: Player):
        for heavy_gunner in self.elements:
            heavy_gunner.control(context, bullets, player)
