import os
import pygame
from base.context import PygameContext
from menu.menu import menu
from game.game import Game
from texts.options_save import OptionsSave

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

options_saving = OptionsSave()
context = PygameContext(1280, 720, options_saving.fullscreen)
game = Game()
run = True
after_game = False
player_name = ""

while run:
    gr, name = menu(context, options_saving, False, after_game, player_name)
    if not gr:
        player_name = game.game(context, options_saving, name)
        after_game = True
    else:
        run = False

pygame.quit()
