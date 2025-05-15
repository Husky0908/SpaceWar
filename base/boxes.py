import random
import pygame
from base.context import PygameContext


class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.form = None
        self.forms = pygame.image.load("Pictures/other_pictures/coin.png")
        self.delete = False

    def draw(self, context: PygameContext):
        self.form = context.screen.blit(self.forms, (self.x, self.y))


class Coins:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for coin in self.elements:
            coin.draw(context)


class PlusHealth:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.form = None
        self.delete = False

    def draw(self, context: PygameContext):
        self.form = pygame.draw.circle(context.screen, (255, 0, 0), (self.x, self.y), 15)


class PlusHealths:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for plus_hp in self.elements:
            plus_hp.draw(context)


class Boxes:
    def __init__(self):
        self.chance = 0

    def small_box(self, coins: Coins, x, y, plus_hp: PlusHealths):
        self.chance = random.randint(1, 10)
        if self.chance > 3:
            if self.chance > 6:
                if self.chance <= 9:
                    coins.elements.append(Coin(x, y, (2 * 10)))
                else:
                    plus_hp.elements.append(PlusHealth(x, y, 1))
            else:
                coins.elements.append(Coin(x, y, (1 * 10)))
