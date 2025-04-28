import pygame
import math
from base.context import PygameContext
from base.directions import get_direction


class Bullet:
    def __init__(self, x_0: int, y_0: int, destination_x: float, destination_y: float, attacker: str):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = x_0
        self.y = y_0
        self.dest_x = destination_x
        self.dest_y = destination_y
        self.dir_x = None
        self.dir_y = None
        self.speed = 400
        self.start_time = 0
        self.sharp = False
        self.form = None
        self.forms = [pygame.image.load("Pictures/players_pictures/player_bullet.png"), pygame.image.load("Pictures/enemies_pictures/bullet_shooters/bullet_shooter_bullet.png")]
        self.r = 10
        self.attacker = attacker

    def control(self, context: PygameContext):
        if self.sharp:
            d_t = context.time - self.start_time
            self.x = self.x_0 + self.dir_x * d_t * self.speed
            self.y = self.y_0 + self.dir_y * d_t * self.speed
            if self.x >= context.width or self.x <= 0 or self.y >= context.height or self.y <= 0:
                self.sharp = False
        else:
            self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
            self.start_time = context.time
            self.sharp = True

    def draw(self, context: PygameContext):
        if self.attacker == "friend":
            self.form = context.screen.blit(self.forms[0], (self.x, self.y))
        else:
            value = math.atan((self.dest_y - self.y_0) / (self.x_0 - self.dest_x)) * 180 / math.pi - 90
            if self.x_0 > self.dest_x:
                value = value - 180

            self.form = context.screen.blit(pygame.transform.rotate(self.forms[1], value), (self.x, self.y))


class Bullets:
    def __init__(self):
        self.last_spawn = 100
        self.elements = []

    def control(self, context: PygameContext):
        self.last_spawn = self.last_spawn + 1
        for bullet in self.elements:
            bullet.control(context)

    def contacts(self):
        for bullet in self.elements:
            tmp_list = []
            for x in self.elements:
                if not x.sharp == False:
                    tmp_list.append(x)
            self.elements = tmp_list

    def draw(self, context: PygameContext):
        for bullet in self.elements:
            bullet.draw(context)
