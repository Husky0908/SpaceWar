import pygame
import random
from base.context import PygameContext


class Tower:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.form = None

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (0, 0, 255), (self.x, self.y, 70, 70))


class Towers:
    def __init__(self):
        self.elements = []

    def spawn(self, context: PygameContext):
        spawn = True
        while spawn:
            x = random.randint(0, context.width - 70)
            y = random.randint(0, context.height - 70)
            spawn_x = True
            spawn_y = True
            spawn = False
            for tower in self.elements:
                if -100 < tower.x - x < 100:
                    spawn_x = False
                if -100 < tower.y - y < 100:
                    spawn_y = False
                if not spawn_x and not spawn_y:
                    spawn = True
                else:
                    spawn_x = True
                    spawn_y = True
        self.elements.append(Tower(x, y))

    def draw(self, context: PygameContext):
        for tower in self.elements:
            tower.draw(context)
