import pygame
from base.context import PygameContext
from menu.menu import menu
from game.game import Game
from texts.options_save import OptionsSave

options_saving = OptionsSave()
context = PygameContext(1280, 720, options_saving.fullscreen)
game = Game()

while not menu(context, options_saving, False):
    game.game(context, options_saving)

pygame.quit()
