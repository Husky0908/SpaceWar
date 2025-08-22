import pygame
from base.context import PygameContext
from texts.text_print import print_text
from texts.options_save import OptionsSave


class Map_and_Upgrades:
    def __init__(self, coin: int, upgrade_box: int, dif: int, ship_name: str, hmm: int):
        self.coin = coin
        self.upgrade_box = upgrade_box
        self.difficulty = dif
        self.ship_name = ship_name
        self.hmm = hmm
        self.map_picture = pygame.image.load("Pictures/menu_pictures/map.png").convert_alpha()
        self.map_background = pygame.image.load("Pictures/menu_pictures/map_background.png").convert_alpha()

    def map(self, context: PygameContext, mouse_form, mouse_click, options_save: OptionsSave, ship):
        context.screen.blit(self.map_background, (0, 0))
        context.screen.blit(self.map_picture, (-10, 0))
        context.screen.blit(ship, (55, 545))
        print_text(self.ship_name, 60, (255, 255, 255), (175, 70), context)
        start_button = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 * 2 + 110), 625, 200, 80))
        print_text((options_save.languages[options_save.select_language])["start"], 45, (0, 0, 0), ((context.width / 4 * 2 + 210), 665), context)
        back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 * 3 + 50), 625, 200, 80))
        print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((context.width / 4 * 3 + 150), 665), context)

        if back_main_menu.colliderect(mouse_form):
            context.screen.blit(ship, ((1280 / 4 * 3 - 15), 625))
        if start_button.colliderect(mouse_form):
            context.screen.blit(ship, ((1280 / 4 * 2 + 45), 625))


        if start_button.colliderect(mouse_form) and mouse_click:
            return "play the game"
        if back_main_menu.colliderect(mouse_form) and mouse_click:
            return "main menu"
        else:
            return "map"
