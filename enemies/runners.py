import pygame
import random
from base.context import PygameContext
from base.player import Player
from base.bullets import Bullets, Bullet
from base.directions import get_direction
from base.boxes import Coins, PlusHealths, Coin, PlusHealth


class Runner:

    height = 110
    width = 50
    STATE_INIT = 0
    STATE_SLOW_MOVE = 1
    STATE_FIRST_STOP = 2
    STATE_FAST_MOVE = 3
    STATE_SECOND_STOP = 4
    STATE_KILLED = 5

    SLOW_SPEED = 80
    FAST_SPEED = 650

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5
        self.state = Runner.STATE_INIT
        self.x_0 = 0
        self.y_0 = 0
        self.dir_x = 0
        self.dir_y = 0
        self.start_time = 0
        self.form = None
        self.forms = [pygame.image.load("Pictures/enemies_pictures/runners/runner_1_hp.png"), pygame.image.load("Pictures/enemies_pictures/runners/runner_2_hp.png"), pygame.image.load("Pictures/enemies_pictures/runners/runner_3_hp.png"), pygame.image.load("Pictures/enemies_pictures/runners/runner_4_hp.png"), pygame.image.load("Pictures/enemies_pictures/runners/runner_5_hp.png")]
        self.wounded = False
        self.r = None
        self.run_time = 0

    def control(self, context: PygameContext, player: Player, coins: Coins, plus_hp: PlusHealths):
        if self.state == Runner.STATE_INIT:
            self.run_time = random.randint(3, 6)
            self.state = Runner.STATE_SLOW_MOVE
            dest_x, dest_y = self.destination(player, 100, 100)
            self.dir_x, self.dir_y = get_direction(self.x, self.y, dest_x, dest_y)
            self.start_time = context.time
            self.x_0, self.y_0 = self.x, self.y
        elif self.state == Runner.STATE_SLOW_MOVE:
            d_t = context.time - self.start_time
            if d_t < self.run_time:
                self.x = self.x_0 + self.dir_x * d_t * Runner.SLOW_SPEED
                self.y = self.y_0 + self.dir_y * d_t * Runner.SLOW_SPEED
            else:
                self.state = Runner.STATE_FIRST_STOP
                self.start_time = context.time
        if self.state == Runner.STATE_FIRST_STOP:
            if context.time - self.start_time >= 3:
                self.state = Runner.STATE_FAST_MOVE
                self.wounded = False
                dest_x, dest_y = self.destination(player, 0, 0)
                dest_x = dest_x
                dest_y = dest_y
                self.dir_x, self.dir_y = get_direction(self.x, self.y, dest_x, dest_y)
                self.start_time = context.time
                self.x_0, self.y_0 = self.x, self.y
        if self.state == Runner.STATE_FAST_MOVE:
            d_t = context.time - self.start_time
            self.x = self.x_0 + self.dir_x * d_t * Runner.FAST_SPEED
            self.y = self.y_0 + self.dir_y * d_t * Runner.FAST_SPEED
            if self.x > context.width - self.width / 2 or self.x < self.width / 2 or self.y > context.height - self.height / 2 or self.y < self.height / 2:
                self.state = Runner.STATE_SECOND_STOP
                self.start_time = context.time
        if self.state == Runner.STATE_SECOND_STOP:
            if context.time - self.start_time >= 3:
                self.state = Runner.STATE_INIT
        if self.health <= 0:
            self.state = Runner.STATE_KILLED
            chance = random.randint(1, 10)
            if chance > 3:
                if chance > 6:
                    if chance <= 9:
                        coins.elements.append(Coin(self.x, self.y, (2 * 10)))
                    else:
                        plus_hp.elements.append(PlusHealth(self.x, self.y, 1))
                else:
                    coins.elements.append(Coin(self.x, self.y, (1 * 10)))

    def draw(self, context: PygameContext):
        self.r = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        if self.health > 0:
            self.form = self.forms[self.health - 1]
        context.screen.blit(self.form, self.r)

    def destination(self, player: Player, width, height):
        rect = player.get_rectangle_around_player(width, height)
        dest_x = random.randint(rect.left, rect.right)
        dest_y = random.randint(rect.top, rect.bottom)
        return dest_x, dest_y

    def contacts(self, player: Player, bullets: Bullets):
        if self.r.colliderect(player.r) and not self.wounded:
            player.health = player.health - 1
            self.wounded = True
        for bullet in bullets.elements:
            if self.r.colliderect(bullet.form) and bullet.attacker == "friend":
                self.health = self.health - 1
                bullet.sharp = False


class Runners:
    def __init__(self):
        self.elements = []


    def control(self, context: PygameContext, player: Player, coins: Coins, plus_hp: PlusHealths):
        for runner in self.elements:
            runner.control(context, player, coins, plus_hp)


    def draw(self, context: PygameContext):
        for runner in self.elements:
            runner.draw(context)


    def spawn(self, context: PygameContext):
        p_o_n = random.randint(1, 2)
        if p_o_n == 1:
            x = 0 - Runner.width
        else:
            x = context.width + Runner.width
        y = random.randint((0 - Runner.height), (context.height + Runner.height))
        self.elements.append(Runner(x, y))


    def contacts(self, player: Player, bullets: Bullets):
        for runner in self.elements:
            runner.contacts(player, bullets)

        tmp_list = []
        for x in self.elements:
            if x.state != Runner.STATE_KILLED:
                tmp_list.append(x)
        self.elements = tmp_list
