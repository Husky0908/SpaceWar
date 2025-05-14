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


class Boxes:
    def __init__(self):
        self.chance = 0

    def small_box(self, coins: Coins, x, y):
        self.chance = random.randint(1, 10)
        if self.chance > 1:
            if self.chance <= 3:
                coins.elements.append(Coin(x, y, (1 * 10)))
            elif self.chance <= 6:
                coins.elements.append(Coin(x, y, (2 * 10)))
            if self.chance >= 7:
                coins.elements.append(Coin(x, y, (3 * 10)))
