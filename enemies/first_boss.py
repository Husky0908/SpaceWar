import pygame
import random
from base.context import PygameContext
from base.directions import get_direction


class FirstBoss:

    STATE_INIT = 0
    STATE_RUNS = 1
    STATE_MOVE = 2
    STATE_SHOOT_BULLETS = 3
    STATE_SHOOT_ROCKETS = 4
    STATE_KILL = 5

    def __init__(self, x: int, y: int):
        self.health = 100
        self.x = x
        self.y = y
        self.x_0 = 0
        self.y_0 = 0
        self.dir_x = 0
        self.dir_y = 0
        self.run_dest = None
        self.start_time = 0
        self.run_number = 0
        self.form = None
        self.live = False
        self.state = FirstBoss.STATE_INIT
        self.width = 370
        self.height = 320

    def spawn(self):
        self.live = True


    def draw(self, context: PygameContext):
        if self.live:
            r = pygame.Rect(self.x, self.y, self.width, self.height)
            self.form = pygame.draw.rect(context.screen, (255, 0, 255), r)

    def control(self, context: PygameContext):
        if self.live:
            if self.state == FirstBoss.STATE_INIT:
                self.y = self.y + 2
                if self.y >= 0:
                    self.run_dest = [((context.width - self.width), (context.height - self.height)), ((context.width - self.width), self.height), (0, (context.height - self.height)), (0, 0)]
                    self.state = FirstBoss.STATE_RUNS
                    self.run_dest_reset(0, context)
            if self.state == FirstBoss.STATE_RUNS:
                d_t = context.time - self.start_time
                if self.run_number == 0:
                    self.run(d_t)
                    if not self.x <= (self.run_dest[self.run_number])[0]:
                        self.run_dest_reset(1, context)
                        self.run_number = self.run_number + 1
                        d_t = context.time - self.start_time
                if self.run_number == 1 and (self.y <= -500 or self.y >= 0):
                    self.run(d_t)
                    if self.y <= 0 and self.y >= -10:
                        self.run_dest_reset(2, context)
                        self.run_number = self.run_number + 1
                        d_t = context.time - self.start_time
                if self.run_number == 2:
                    self.run(d_t)
                    if self.x <= 0:
                        self.run_dest_reset(3, context)
                        self.run_number = self.run_number + 1
                        d_t = context.time - self.start_time
                if self.run_number == 3:
                    self.run(d_t)
                    if self.y <= -self.height:
                        self.state = FirstBoss.STATE_MOVE


    def run(self, d_t):
        self.x = self.x_0 + self.dir_x * d_t * 500
        self.y = self.y_0 + self.dir_y * d_t * 500

    def run_dest_reset(self, number, context: PygameContext):
        self.dir_x, self.dir_y = get_direction(self.x, self.y, (self.run_dest[number])[0], (self.run_dest[number])[1])
        self.start_time = context.time
        self.x_0, self.y_0 = self.x, self.y
