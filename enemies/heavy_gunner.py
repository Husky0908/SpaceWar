import pygame
import random
from base.context import PygameContext
from base.directions import get_direction


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

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (0, 0, 255), (self.x, self.y, 75, 75))

    def control(self, context: PygameContext):
        if self.state == HeavyGunner.STATE_INIT:
            self.y = self.y + 2
            if self.y >= 25:
                self.state = HeavyGunner.STATE_WHERE_MOVE
                self.moving = random.randint(3, 4)
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
                self.state = HeavyGunner.STATE_WHERE_MOVE


class HeavyGunners:
    def __init__(self):
        self.elements = []

    def spawn(self):
        self.elements.append(HeavyGunner())

    def draw(self, context: PygameContext):
        for heavy_gunner in self.elements:
            heavy_gunner.draw(context)

    def control(self, context: PygameContext):
        for heavy_gunner in self.elements:
            heavy_gunner.control(context)
