import pygame
import math
import random
from base.context import PygameContext
from base.player import Player
from base.directions import get_direction


class Rocket:

    height = 25
    width = 25
    STATE_MOVE = 1
    STATE_DESTROY = 2

    def __init__(self, x: int, y: int, attacker: str):
        self.x = x
        self.y = y
        self.health = 1
        self.dest_x = None
        self.dest_y = None
        self.dir_x = None
        self.dir_y = None
        self.speed = 3
        self.form = None
        self.forms = [pygame.image.load("Pictures/enemies_pictures/rocket_launchers/rocket_launcher_rocket.png")]
        self.r = 10
        self.attacker = attacker
        self.state = Rocket.STATE_MOVE
        self.time = 0

    def control(self, player: Player):
        if self.state == Rocket.STATE_MOVE:
            self.dest_x = player.x
            self.dest_y = player.y
            self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
            self.x = self.x + self.dir_x * self.speed
            self.y = self.y + self.dir_y * self.speed
        if self.health <= 0:
            self.state = Rocket.STATE_DESTROY

    def contacts(self, player: Player):
        if self.form.colliderect(player.r):
            if player.ship_power == 2:
                shield = random.randint(0, 100)
                if shield <= 5:
                    player.health = player.health + 1
            self.state = Rocket.STATE_DESTROY
            player.health = player.health - 1

    def draw(self, context: PygameContext):
        r = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        value = math.atan((self.dest_y - self.y) / (self.x - self.dest_x)) * 180 / math.pi - 90
        if self.x > self.dest_x:
            value = value - 180
        self.form = context.screen.blit(pygame.transform.rotate(self.forms[0], value), (self.x, self.y))
        #self.form = pygame.draw.rect(context.screen, (230, 0, 100), r)


class Rockets:
    def __init__(self):
        self.elements = []

    def spawn(self, x, y, attacker):
        self.elements.append(Rocket(x, y, attacker))

    def control(self, player: Player):
        for rocket in self.elements:
            rocket.control(player)

    def contacts(self, player: Player):
        for rocket in self.elements:
            rocket.contacts(player)

        for rocket in self.elements:
            tmp_list = []
            for x in self.elements:
                if not x.state == Rocket.STATE_DESTROY:
                    tmp_list.append(x)
            self.elements = tmp_list

    def draw(self, context: PygameContext):
        for rocket in self.elements:
            rocket.draw(context)
