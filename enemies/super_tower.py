import pygame
import random
from base.context import PygameContext
from base.bullets import Bullets, Bullet


class SuperTower:
    STATE_INIT = 0
    STATE_SHOOT_RANDOM = 1
    STATE_SHOOT_SIDE = 2
    STATE_SHOOT_LASER = 3

    def __init__(self, dif):
        self.health = 125 + (dif * 25)
        self.x = 465
        self.y = -350
        self.live = False
        self.form = None
        self.state = SuperTower.STATE_INIT
        self.shoot_time = 0
        self.shoot_time_end = 5

    def draw(self, context: PygameContext):
        if self.live:
            self.form = pygame.draw.rect(context.screen, (255, 255, 0), (self.x, self.y, 350, 350))

    def control(self, bullets: Bullets):
        if self.live:
            if self.state == SuperTower.STATE_INIT:
                self.y = self.y + 2.5
                if self.y >= 185:
                    self.state = 1  # random.randint(1, 3)
            if self.state == SuperTower.STATE_SHOOT_RANDOM:
                self.shoot_time = self.shoot_time + 1
                if self.shoot_time >= self.shoot_time_end:
                    self.shoot_time = 0
                    plus_x = random.randint(-100, 100)
                    if plus_x == 0:
                        plus_x = plus_x + 1
                    plus_x = (self.x + 175) + plus_x
                    plus_y = (self.y + 175) + random.randint(-100, 100)
                    # if plus_y == 0:
                    #     plus_y = plus_y - 1
                    bullets.elements.append(Bullet(self.x + 175, self.y + 175, plus_x, plus_y, "enemy", 400))

    def spawn(self):
        self.live = True
