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
        self.forms = pygame.image.load("Pictures/other_pictures/player_plus_health.png")
        self.delete = False

    def draw(self, context: PygameContext):
        self.form = context.screen.blit(self.forms, (self.x, self.y))


class PlusHealths:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for plus_hp in self.elements:
            plus_hp.draw(context)
