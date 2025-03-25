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
    STATE_SECOND_MOVE = 5
    STATE_KILL = 6

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
        self.side = None
        self.form = None
        self.bullet_shooter_form = None
        self.bullet_shooter_live = False
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
            if self.bullet_shooter_live:
                if self.side == 2:
                    r = pygame.Rect((self.x - 60), ((self.y + (self.height / 2)) - 30), 60, 60)
                else:
                    r = pygame.Rect((self.x + self.width), ((self.y + (self.height / 2)) - 30), 60, 60)
                self.bullet_shooter_form = pygame.draw.rect(context.screen, (0, 0, 255), r)

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
                    if not self.x <= (context.width - self.width):
                        self.run_dest_reset(1, context)
                        self.run_number = self.run_number + 1
                        d_t = context.time - self.start_time
                if self.run_number == 1:
                    self.run(d_t)
                    if self.y <= 0:
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
                        self.side = random.randint(1, 2)
                        if self.side == 1:
                            self.x = 0 - self.width
                        else:
                            self.x = context.width
                        self.y = (context.height / 2) - (self.height / 2)
            if self.state == FirstBoss.STATE_MOVE:
                if self.side == 1:
                    self.x = self.x + 5
                else:
                    self.x = self.x - 5
                if (context.width - self.width) >= self.x >= 0:
                    shoot = random.randint(1, 2)
                    shoot = 1
                    if shoot == 1:
                        self.state = FirstBoss.STATE_SHOOT_BULLETS
                        self.bullet_shooter_live = True
                    else:
                        self.state = FirstBoss.STATE_SHOOT_ROCKETS
                    self.start_time = context.time
            if self.state == FirstBoss.STATE_SHOOT_BULLETS:
                d_t = context.time - self.start_time
                if d_t >= 4:
                    self.state = FirstBoss.STATE_SECOND_MOVE
                    self.bullet_shooter_live = False
            if self.state == FirstBoss.STATE_SECOND_MOVE:
                if self.side == 1:
                    self.x = self.x + 8
                else:
                    self.x = self.x - 8
                if self.x >= (context.width + self.width) or self.x <= (0 - self.width):
                    self.state = FirstBoss.STATE_INIT
                    self.x = 0
                    self.y = -350


    def run(self, d_t):
        self.x = self.x_0 + self.dir_x * d_t * 500
        self.y = self.y_0 + self.dir_y * d_t * 500

    def run_dest_reset(self, number, context: PygameContext):
        self.dir_x, self.dir_y = get_direction(self.x, self.y, (self.run_dest[number])[0], (self.run_dest[number])[1])
        self.start_time = context.time
        self.x_0, self.y_0 = self.x, self.y
