import pygame
from texts.text_print import print_text
from base.context import PygameContext
from texts.options_save import OptionsSave

def menu(context: PygameContext) -> bool:
    ## TODO: context-et hasznalni menu_screen helyett
    ## meg a clock helyett is
    menu_screen = pygame.display.set_mode((1280, 720))
    menu_clock = pygame.time.Clock()

    mouse_press_time = 0

    options_save = OptionsSave()
    which_menu = "main menu"

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    ship = pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha()
    options_controls = pygame.image.load("Pictures/menu_pictures/options_controls.png").convert_alpha()

    running = True
    must_quit = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                must_quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            else:
                mouse_click = False
        mouse_press_time = mouse_press_time + 1
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_ESCAPE] and esc:
        #     return None

        menu_screen.fill((0, 0, 0))

        mouse_form = pygame.draw.circle(menu_screen, (255, 255, 255), pygame.mouse.get_pos(), 10)
        if which_menu == "main menu":
            play_game = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 2 - 100), 200, 200, 80))
            print_text((options_save.languages[options_save.select_language])["play"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            options = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 2 - 100), 325, 200, 80))
            print_text((options_save.languages[options_save.select_language])["options"], 45, (0, 0, 0), ((1280 / 2), 365), context)
            game_quit = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 2 - 100), 450, 200, 80))
            print_text((options_save.languages[options_save.select_language])["quit"], 45, (0, 0, 0), ((1280 / 2), 490), context)

            if play_game.colliderect(mouse_form):
                menu_screen.blit(ship,((1280 / 2 - 165), 200))
            if options.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 325))
            if game_quit.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 450))
            if play_game.colliderect(mouse_form) and mouse_click:
                running = False
            if options.colliderect(mouse_form) and mouse_click:
                which_menu = "options"
            if game_quit.colliderect(mouse_form) and mouse_click:
                running = False
                must_quit = True

        if which_menu == "options":
            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            print_text((options_save.languages[options_save.select_language])["language"], 45, (255, 255, 255), ((1280 / 3), 150), context)
            language_button = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 3 * 2 - 75), 125, 150, 50))
            if 1 == options_save.how_number:
                options_save.select_language = "English"
            else:
                options_save.select_language = "Magyar"
            print_text(options_save.select_language, 45, (0, 0, 0), ((1280 / 3 * 2), 150), context)
            #menu_screen.blit(options_controls, (330, 100))
            back_main_menu = pygame.draw.rect(menu_screen, (255, 255, 255), (540, 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 2), 590), context)

            if back_main_menu.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 550))
            if language_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                options_save.how_number = options_save.how_number + 1
                mouse_press_time = 0
            if options_save.how_number >= len(options_save.languages.keys()):
                options_save.how_number = 0
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"

        pygame.display.flip()
        menu_clock.tick(60)

    return must_quit

#menu(False)
