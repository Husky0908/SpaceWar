import pygame
from base.context import PygameContext
from base.directions import get_direction


class Bomb:
    STATE_MOVE = 1
    STATE_EXPLOSION = 2

    def __init__(self, x_0: float, y_0: float, dest_x: float, dest_y: float, attacker: str):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = x_0
        self.y = y_0
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.dir_x = None
        self.dir_y = None
        self.speed = 10
        self.start_time = 0
        self.sharp = False
        self.form = None
        self.r = 10
        self.attacker = attacker
        self.state = Bomb.STATE_MOVE

    def draw(self, context: PygameContext):
        if self.state == Bomb.STATE_MOVE:
            self.form = pygame.draw.circle(context.screen, (255, 0, 0), (self.x, self.y), self.r)
        else:
            self.r = 60
            self.form = pygame.draw.circle(context.screen, (255, 0, 0), (self.x, self.y), self.r)

    def control(self, context: PygameContext):
        if self.state == Bomb.STATE_MOVE:
            if self.sharp:
                d_t = context.time - self.start_time
                self.x = self.x + self.dir_x * self.speed
                self.y = self.y + self.dir_y * self.speed
                if d_t >= 10:
                    self.speed = self.speed - 2.5
                    self.start_time = context.time
                if self.x >= context.width or self.x <= 0 or self.y >= context.height or self.y <= 0:
                    self.sharp = False
            else:
                self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.start_time = context.time
                self.sharp = True


class Bombs:
    def __init__(self, context: PygameContext):
        self.last_spawn = context.time + 300
        self.elements = []

    def draw(self, context: PygameContext):
        for bomb in self.elements:
            bomb.draw(context)

    def control(self, context: PygameContext):
        self.last_spawn = self.last_spawn + 1
        for bomb in self.elements:
            bomb.control(context)

    def contacts(self):
        tmp_list = []
        for x in self.elements:
            if x.sharp:
                tmp_list.append(x)
        self.elements = tmp_list
