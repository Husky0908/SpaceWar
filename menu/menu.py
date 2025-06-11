import pygame
import os
from texts.text_print import print_text
from base.context import PygameContext
from texts.options_save import OptionsSave


def _get_key_code() -> int | None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.unicode == chr(pygame.K_ESCAPE) or event.unicode == chr(pygame.K_BACKSPACE):
                    return None
                else:
                    return event.key


def menu(context: PygameContext, options_save: OptionsSave, escape: bool) -> bool:
    mouse_press_time = 0

    options_save.saving_reading()
    which_menu = "main menu"

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    ship = pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha()
    credits_eng = pygame.image.load("Pictures/menu_pictures/credits_eng.png").convert_alpha()
    credits_hun = pygame.image.load("Pictures/menu_pictures/credits_hun.png").convert_alpha()

    running = True
    must_quit = False
    which_control = ""
    new_ship_name = ""

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
            print_text("SpaceWar", 120, (0, 0, 255), ((1280 / 2), 100), context)
            print_text("Alpha 0.1.", 45, (255, 255, 255), ((1280 / 3 * 2), 150), context)
            play_game = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 200, 200, 80))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["play"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            else:
                print_text((options_save.languages[options_save.select_language])["continue"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            credits = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 325, 200, 80))
            print_text((options_save.languages[options_save.select_language])["credits"], 45, (0, 0, 0), ((1280 / 2), 365), context)
            options = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 450, 200, 80))
            print_text((options_save.languages[options_save.select_language])["options"], 45, (0, 0, 0), ((1280 / 2), 490), context)
            game_quit = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 575, 200, 80))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["quit"], 45, (0, 0, 0), ((1280 / 2), 615), context)
            else:
                print_text((options_save.languages[options_save.select_language])["finish"], 45, (0, 0, 0), ((1280 / 2), 615), context)

            if play_game.colliderect(mouse_form):
                context.screen.blit(ship,((1280 / 2 - 165), 200))
            if credits.colliderect(mouse_form):
                context.screen.blit(ship,((1280 / 2 - 165), 325))
            if options.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 450))
            if game_quit.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 575))
            if play_game.colliderect(mouse_form) and mouse_click:
                which_menu = "players"
                mouse_click = False
                # if not escape:
                #     context.time = 0
                #     running = False
                # else:
                #     return False
            if credits.colliderect(mouse_form) and mouse_click:
                which_menu = "credits"
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
            game_options_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 200, 200, 80))
            print_text((options_save.languages[options_save.select_language])["game"], 45, (0, 0, 0), ((1280 / 2), 240), context)
            controls_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 2 - 100), 325, 200, 80))
            print_text((options_save.languages[options_save.select_language])["controls"], 45, (0, 0, 0), ((1280 / 2), 365), context)
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), (540, 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 2), 590), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 550))
            if game_options_button.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 200))
            if controls_button.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 325))
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"
            if game_options_button.colliderect(mouse_form) and mouse_click:
                which_menu = "game options"
            if controls_button.colliderect(mouse_form) and mouse_click:
                which_menu = "controls"
                get_input = False

        if which_menu == "game options":
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
                pygame.display.set_icon(ship)
            if options_save.how_number >= len(options_save.languages.keys()):
                options_save.how_number = 0
            if not escape:
                if difficulty_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    options_save.game_difficulty = options_save.game_difficulty + 1
                    mouse_press_time = 0
            if options_save.game_difficulty > 1:
                options_save.game_difficulty = -1
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "options"
                options_save.saving_writing()

        if which_menu == "controls":
            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), (540, 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 2), 590), context)
            print_text((options_save.languages[options_save.select_language])["up"], 45, (255, 255, 255), ((1280 / 3), 150), context)
            up_control_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 + 100), 125, 150, 50))
            print_text((options_save.languages[options_save.select_language])["down"], 45, (255, 255, 255), ((1280 / 3), 250), context)
            down_control_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 + 100), 225, 150, 50))
            print_text((options_save.languages[options_save.select_language])["left"], 45, (255, 255, 255), ((1280 / 3 * 2), 150), context)
            left_control_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 + 100), 125, 150, 50))
            print_text((options_save.languages[options_save.select_language])["right"], 45, (255, 255, 255), ((1280 / 3 * 2), 250), context)
            right_control_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 + 100), 225, 150, 50))

            if not pygame.key.name(options_save.up_control, use_compat=True) == "":
                print_text(pygame.key.name(options_save.up_control, use_compat=True), 45, (0, 0, 0), ((1280 / 3 + 175), 150), context)
            else:
                print_text("*", 45, (0, 0, 0), ((1280 / 3 + 175), 150), context)
            if not pygame.key.name(options_save.left_control, use_compat=True) == "":
                print_text(pygame.key.name(options_save.left_control, use_compat=True), 45, (0, 0, 0), ((1280 / 3 * 2 + 175), 150), context)
            else:
                print_text("*", 45, (0, 0, 0), ((1280 / 3 * 2 + 175), 150), context)
            if not pygame.key.name(options_save.down_control, use_compat=True) == "":
                print_text(pygame.key.name(options_save.down_control, use_compat=True), 45, (0, 0, 0), ((1280 / 3 + 175), 250), context)
            else:
                print_text("*", 45, (0, 0, 0), ((1280 / 3 + 175), 250), context)
            if not pygame.key.name(options_save.right_control, use_compat=True) == "":
                print_text(pygame.key.name(options_save.right_control, use_compat=True), 45, (0, 0, 0), ((1280 / 3 * 2 + 175), 250), context)
            else:
                print_text("*", 45, (0, 0, 0), ((1280 / 3 * 2 + 175), 250), context)

            if not get_input:
                if back_main_menu.colliderect(mouse_form):
                    context.screen.blit(ship, ((1280 / 2 - 165), 550))
                if up_control_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    mouse_press_time = 0
                    get_input = True
                    which_control = "up"
                    print_text((options_save.languages[options_save.select_language])["press"], 45, (255, 255, 255), ((1280 / 3 + 175), 100), context)
                if down_control_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    mouse_press_time = 0
                    get_input = True
                    which_control = "down"
                    print_text((options_save.languages[options_save.select_language])["press"], 45, (255, 255, 255), ((1280 / 3 + 175), 200), context)
                if left_control_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    mouse_press_time = 0
                    get_input = True
                    which_control = "left"
                    print_text((options_save.languages[options_save.select_language])["press"], 45, (255, 255, 255), ((1280 / 3 * 2 + 175), 100), context)
                if right_control_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    mouse_press_time = 0
                    get_input = True
                    which_control = "right"
                    print_text((options_save.languages[options_save.select_language])["press"], 45, (255, 255, 255), ((1280 / 3 * 2 + 175), 200), context)
                if back_main_menu.colliderect(mouse_form) and mouse_click:
                    which_menu = "options"
                    options_save.saving_writing()
            else:
                key = _get_key_code()
                get_input = False
                if key is not None:
                    if which_control == "up":
                        options_save.up_control = key
                    if which_control == "down":
                        options_save.down_control = key
                    if which_control == "left":
                        options_save.left_control = key
                    if which_control == "right":
                        options_save.right_control = key

        if which_menu == "credits":
            if options_save.select_language == "English":
                context.screen.blit(credits_eng, (0, 0))
            else:
                context.screen.blit(credits_hun, (0, 0))
            print_text((options_save.languages[options_save.select_language])["credits"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), (540, 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 2), 590), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 2 - 165), 550))
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"

        if which_menu == "players":
            players = os.listdir("texts/players")
            how_many = 1
            how_many_2 = 1
            print_text((options_save.languages[options_save.select_language])["players"], 80, (255, 255, 255), ((1280 / 2), 100), context)

            for player_name in players:
                if how_many_2 == 1:
                    player_box = pygame.draw.rect(context.screen, (255, 255, 0), ((how_many * context.width / 5), (how_many_2 * 200 - 50), 200, 200))
                    print_text(player_name, 45, (0, 0, 0), ((how_many * (context.width / 5) + 100), (how_many_2 * 200 + 50)), context)
                else:
                    player_box = pygame.draw.rect(context.screen, (255, 255, 0), ((how_many * context.width / 5), (how_many_2 * 200), 200, 200))
                    print_text(player_name, 45, (0, 0, 0), ((how_many * (context.width / 5) + 100), (how_many_2 * 200 + 100)), context)
                how_many = how_many + 1
                if how_many == 4:
                    how_many = 1
                    how_many_2 = 2
                if player_box.colliderect(mouse_form) and mouse_click:
                    if not escape:
                        context.time = 0
                        running = False
                    else:
                        return False

            new_ship = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 5 - 200), 625, 400, 80))
            print_text((options_save.languages[options_save.select_language])["create"], 45, (0, 0, 0), ((context.width / 5), 665), context)
            delete_ship = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 5 * 3 - 235), 625, 400, 80))
            print_text((options_save.languages[options_save.select_language])["delete"], 45, (0, 0, 0), ((context.width / 5 * 3 - 35), 665), context)
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 * 3 + 50), 625, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((context.width / 4 * 3 + 150), 665), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(ship, ((1280 / 4 * 3 - 15), 625))

            if new_ship.colliderect(mouse_form) and mouse_click:
                which_menu = "new ship"
                new_ship_name = ""
                get_key = False
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"

        if which_menu == "new ship":
            print_text((options_save.languages[options_save.select_language])["create"], 80, (255, 255, 255), ((1280 / 2), 100), context)
            name_button = pygame.draw.rect(context.screen, (255, 255, 0), ((context.width / 2 - 100), 550, 200, 80))
            back_main_menu = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 * 3 - 100), 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (0, 0, 0), ((1280 / 4 * 3), 590), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(ship, ((context.width / 4 * 3 - 165), 550))
            if name_button.colliderect(mouse_form) and mouse_click:
                get_key = True
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "players"

            if get_key:
                typing = True
                while typing:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.unicode == chr(pygame.K_ESCAPE) or event.unicode == chr(pygame.K_BACKSPACE) or event.unicode == chr(pygame.K_RETURN):
                                if event.unicode == chr(pygame.K_BACKSPACE):
                                    if len(new_ship_name) > 0:
                                        new_ship_name = new_ship_name.strip(new_ship_name[len(new_ship_name) - 1])
                                else:
                                    get_key = False
                                typing = False
                            else:
                                typing = False
                                new_ship_name = new_ship_name + chr(event.key)
            print_text(new_ship_name, 45, (255, 255, 255), (100, 100), context)

        pygame.display.flip()
        context.delta_time = context.clock.tick(60) / 1000

    return must_quit
