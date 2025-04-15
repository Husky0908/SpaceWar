import pygame
from texts.text_print import print_text
from base.context import PygameContext
from texts.options_save import OptionsSave

def menu(context: PygameContext, options_save: OptionsSave, escape) -> bool:
    mouse_press_time = 0

    options_save.saving_reading()
    which_menu = "main menu"

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    ship = pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha()

    running = True
    must_quit = False

    while running:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                must_quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        mouse_press_time = mouse_press_time + 1

        context.screen.fill((0, 0, 0))

        mouse_form = pygame.draw.circle(context.screen, (255, 255, 255), pygame.mouse.get_pos(), 10)
        if which_menu == "main menu":
            play_game = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 200, 200, 80))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["play"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            else:
                print_text((options_save.languages[options_save.select_language])["continue"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            options = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 325, 200, 80))
            print_text((options_save.languages[options_save.select_language])["options"], 45, (0, 0, 0), ((1280 / 2), 365), context)
            game_quit = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 450, 200, 80))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["quit"], 45, (0, 0, 0), ((1280 / 2), 490), context)
            else:
                print_text((options_save.languages[options_save.select_language])["finish"], 45, (0, 0, 0), ((1280 / 2), 490), context)

            if play_game.colliderect(mouse_form):
                context.screen.blit(ship,((1280 / 2 - 165), 200))
            if options.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 325))
            if game_quit.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 450))
            if play_game.colliderect(mouse_form) and mouse_click:
                if not escape:
                    running = False
                else:
                    return False
            if options.colliderect(mouse_form) and mouse_click:
                which_menu = "options"
            if game_quit.colliderect(mouse_form) and mouse_click:
                if not escape:
                    running = False
                    must_quit = True
                else:
                    return True

        if which_menu == "options":
            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            print_text((options_save.languages[options_save.select_language])["language"], 45, (255, 255, 255), ((1280 / 3), 150), context)
            print_text((options_save.languages[options_save.select_language])["fullscreen"], 45, (255, 255, 255), ((1280 / 3), 250), context)
            if not escape:
                print_text((options_save.languages[options_save.select_language])["difficulty"], 45, (255, 255, 255), ((1280 / 3), 350), context)
                difficulty_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 - 75), 325, 150, 50))
            language_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 - 75), 125, 150, 50))
            fullscreen_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 - 75), 225, 150, 50))
            if options_save.fullscreen:
                print_text((options_save.languages[options_save.select_language])["on"], 45, (0, 0, 0), (((1280 / 3) * 2), 250), context)
            else:
                print_text((options_save.languages[options_save.select_language])["off"], 45, (0, 0, 0), (((1280 / 3) * 2), 250), context)
            if 1 == options_save.how_number:
                options_save.select_language = "English"
            else:
                options_save.select_language = "Magyar"
            print_text(options_save.select_language, 45, (0, 0, 0), ((1280 / 3 * 2), 150), context)
            if not escape:
                if options_save.game_difficulty == 1:
                    d = (options_save.languages[options_save.select_language])["hard"]
                if options_save.game_difficulty == 0:
                    d = (options_save.languages[options_save.select_language])["normal"]
                if options_save.game_difficulty == -1:
                    d = (options_save.languages[options_save.select_language])["easy"]
                print_text(d, 45, (0, 0, 0), ((1280 / 3 * 2), 350), context)
            #menu_screen.blit(options_controls, (330, 100))
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), (540, 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 2), 590), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 550))
            if language_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                options_save.how_number = options_save.how_number + 1
                mouse_press_time = 0
            if fullscreen_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                mouse_press_time = 0
                if options_save.fullscreen:
                    options_save.fullscreen = False
                else:
                    options_save.fullscreen = True
                pygame.display.toggle_fullscreen()
            if options_save.how_number >= len(options_save.languages.keys()):
                options_save.how_number = 0
            if not escape:
                if difficulty_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    options_save.game_difficulty = options_save.game_difficulty + 1
                    mouse_press_time = 0
            if options_save.game_difficulty > 1:
                options_save.game_difficulty = -1
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"
                options_save.saving_writing()

        pygame.display.flip()
        context.delta_time = context.clock.tick(60) / 1000

    return must_quit
