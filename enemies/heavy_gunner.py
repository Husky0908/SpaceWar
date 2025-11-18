import pygame
import random
import math
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
        if self.state == HeavyGunner.STATE_SHOOT:
            bullets.elements.append(Bullet(self.x, self.y, self.player_x, self.player_y, "enemy"))
            delta_x, delta_y = get_delta_vector(self.x, self.y, self.player_x, self.player_y)
            # delta_x = abs(self.x - self.player_x)
            # delta_y = abs(self.y - self.player_y)
            # print(dir_x, dir_y)
            # print(math.atan2(dir_x, dir_y))
            # print(math.degrees(math.atan(dir_y)))
            negative = (delta_y < 0)
            yf1 = self.y + ((delta_y + 0.5773 * delta_x)/(1 - (delta_y / delta_x) * 0.5773))
            xf1 = self.player_x
            if (negative and yf1 > 0) or (not negative and yf1 < 0):
                yf1 = -1 * yf1
                xf1 = -1 * xf1
            bullets.elements.append(Bullet(self.x, self.y, xf1, yf1, "enemy"))
            yf2 = self.y + ((delta_y - 0.5773 * delta_x)/(1 + (delta_y / delta_x) * 0.5773))
            xf2 = self.player_x
            if (negative and yf2 > 0) or (not negative and yf2 < 0):
                yf2 = -1 * yf2
                xf2 = -1 * xf2
            bullets.elements.append(Bullet(self.x, self.y, xf2, yf2, "enemy"))


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
