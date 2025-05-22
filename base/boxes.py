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

    def control(self, context: PygameContext):
        self.y = self.y + 0.5
        if self.y >= context.height:
            self.delete = True


class Coins:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for coin in self.elements:
            coin.draw(context)

    def control(self, context: PygameContext):
        for coin in self.elements:
            coin.control(context)

        tmp_list = []
        for coin in self.elements:
            if not coin.delete:
                tmp_list.append(coin)
            self.elements = tmp_list


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

    def control(self, context: PygameContext):
        self.y = self.y + 0.5
        if self.y >= context.height:
            self.delete = True


class PlusHealths:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for plus_hp in self.elements:
            plus_hp.draw(context)

    def control(self, context: PygameContext):
        for plus_h in self.elements:
            plus_h.control(context)

        tmp_list = []
        for plus_h in self.elements:
            if not plus_h.delete:
                tmp_list.append(plus_h)
        self.elements = tmp_list


class Upgrader:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.form = None
        self.forms = pygame.image.load("Pictures/other_pictures/upgrader_box.png")
        self.delete = False

    def draw(self, context: PygameContext):
        self.form = context.screen.blit(self.forms, (self.x, self.y))

    def control(self, context: PygameContext):
        self.y = self.y + 0.5
        if self.y >= context.height:
            self.delete = True


class Upgraders:
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for upgrade in self.elements:
            upgrade.draw(context)

    def control(self, context: PygameContext):
        for upgrade in self.elements:
            upgrade.control(context)

        tmp_list = []
        for upgrade in self.elements:
            if not upgrade.delete:
                tmp_list.append(upgrade)
        self.elements = tmp_list
