import pygame

from base.context import PygameContext

from menu.menu import menu
from game.game import game


context = PygameContext(1280, 720)

while not menu(context):
    game(context)
    

pygame.quit()

