import pygame
from base.context import PygameContext
from menu.menu import menu
from game.game import game
from texts.options_save import OptionsSave


context = PygameContext(1280, 720)
options_saving = OptionsSave()

while not menu(context, options_saving):
    game(context, options_saving)

pygame.quit()
