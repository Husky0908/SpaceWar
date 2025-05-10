import random
import pygame
from base.context import PygameContext


class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.form = None

    def draw(self, context: PygameContext):
        self.form = pygame.draw.circle(context.screen, (255, 0, 0), (self.x, self.y), 10)


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
        self.chance = random.randint(2, 3)
        if self.chance > 1:
            if self.chance <= 3:
                coins.elements.append(Coin(x, y, (self.chance * 10)))
