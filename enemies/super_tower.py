import pygame
import random
import math
from base.context import PygameContext
from base.bullets import Bullets, Bullet


class SuperTower:
    STATE_INIT = 0
    STATE_SHOOT_RANDOM = 1
    STATE_SHOOT_LASER = 2

    def __init__(self, dif):
        self.health = 125 + (dif * 25)
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
        self.circle_r = math.sqrt(((1280 / 2) ** 2) + ((720 / 2) ** 2))
        self.laser_direction = 1

    def draw(self, context: PygameContext):
        if self.live:
            self.form = pygame.draw.rect(context.screen, (255, 255, 0), (self.x, self.y, 350, 350))

            if self.laser_live:
                self.laser_form = pygame.draw.line(context.screen, (0, 0, 255), (self.x + 175, self.y + 175), self.laser_end_position, 10)

    def control(self, bullets: Bullets, context: PygameContext):
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

    def spawn(self):
        self.live = True
