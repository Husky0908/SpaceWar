import pygame
import random
from base.context import PygameContext
from base.player import Player
from base.bullets import Bullet
from base.directions import get_direction, length
from base.rockets import Rockets


class RocketLauncher:

    height = 50
    width = 50
    STATE_INIT = 0
    STATE_MOVE = 1
    STATE_WAIT = 2
    STATE_SHOOT = 3
    STATE_KILL = 4

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.x_0 = x
        self.y_0 = y
        self.dest_x = None
        self.dest_y = None
        self.dir_x = None
        self.dir_y = None
        self.health = 4
        self.STATE = RocketLauncher.STATE_INIT
        self.form = None
        self.start_time = 0
        self.speed = 75


    def draw(self, context: PygameContext):
        r = pygame.Rect(self.x - self.width / 2,
                        self.y - self.height / 2, self.width,
                        self.height)
        self.form = pygame.draw.rect(context.screen, (200, 200, 200), r)


    def control(self, context: PygameContext, player: Player, rockets: Rockets):
        if self.STATE == RocketLauncher.STATE_INIT:
            self.y = self.y + self.speed / 40
            if self.y >= 50:
                self.STATE = RocketLauncher.STATE_MOVE
                trying = True
                while trying:
                    self.dest_x = random.randint((0 + RocketLauncher.width // 2),
                                                            context.width - RocketLauncher.width // 2)
                    self.dest_y = random.randint(0 + RocketLauncher.height // 2,
                                                            context.height - RocketLauncher.height // 2)
                    leng = length(player.x, self.dest_x, player.y, self.dest_y)
                    if leng >= 600:
                        trying = False
                        self.start_time = context.time
                        self.x_0, self.y_0 = self.x, self.y
                        self.dir_x, self.dir_y = get_direction(self.x_0, self.y_0, self.dest_x, self.dest_y)
                        self.time = random.randint(1, 4)
        if self.STATE == RocketLauncher.STATE_MOVE:
            d_t = context.time - self.start_time
            if d_t < self.time:
                self.x = self.x_0 + self.dir_x * d_t * self.speed
                self.y = self.y_0 + self.dir_y * d_t * self.speed
            else:
                self.STATE = RocketLauncher.STATE_WAIT
                self.start_time = context.time
                self.time = random.randint(1, 4)
        if self.STATE == RocketLauncher.STATE_WAIT:
            if context.time - self.start_time >= self.time:
                self.STATE = RocketLauncher.STATE_SHOOT
        if self.STATE == RocketLauncher.STATE_SHOOT:
            rockets.spawn(self.x, self.y, "enemy")
            self.STATE = RocketLauncher.STATE_INIT
        if self.health <= 0:
            self.STATE = RocketLauncher.STATE_KILL


    def contacts(self, bullet: Bullet):
        if bullet.form.colliderect(self.form) and bullet.attacker == "friend":
            bullet.sharp = False
            self.health = self.health - 1


class RocketLaunchers:
    def __init__(self):
        self.elements = []


    def spawn(self, context: PygameContext):
        x = random.randint(0, context.width)
        y = -RocketLauncher.height
        self.elements.append(RocketLauncher(x, y))


    def draw(self, context: PygameContext):
        for rocket_launcher in self.elements:
            rocket_launcher.draw(context)

    def control(self, context: PygameContext, player: Player, rockets: Rockets):
        for rocket_launcher in self.elements:
            rocket_launcher.control(context, player, rockets)

    def contacts(self, bullet: Bullet):
        for rocket_launcher in self.elements:
            rocket_launcher.contacts(bullet)

        for rocket_launcher in self.elements:
            tmp_list = []
            for x in self.elements:
                if not x.STATE == RocketLauncher.STATE_KILL:
                    tmp_list.append(x)
            self.elements = tmp_list