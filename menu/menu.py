import pygame
import os
from texts.text_print import print_text
from base.context import PygameContext
from texts.options_save import OptionsSave
from menu.map_and_upgrades import Map_and_Upgrades


def _get_key_code() -> int | None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.unicode == chr(pygame.K_ESCAPE) or event.unicode == chr(pygame.K_BACKSPACE):
                    return None
                else:
                    return event.key


def menu(context: PygameContext, options_save: OptionsSave, escape: bool, after_game: bool, player_name: str) -> bool:
    mouse_press_time = 0

    options_save.saving_reading()
    if after_game:
        mau = Map_and_Upgrades(player_name)
        which_menu = "map"
        unlock_player_name = player_name
    else:
        which_menu = "main menu"
        unlock_player_name = ""

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    ship = pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha()
    credits_eng = pygame.image.load("Pictures/menu_pictures/credits_eng.png").convert_alpha()
    credits_hun = pygame.image.load("Pictures/menu_pictures/credits_hun.png").convert_alpha()
    button_plate = pygame.image.load("Pictures/menu_pictures/button_plate.png").convert_alpha()
    button_plate_on = pygame.image.load("Pictures/menu_pictures/button_plate_on.png").convert_alpha()
    big_button_plate = pygame.image.load("Pictures/menu_pictures/big_button_plate.png").convert_alpha()
    big_button_plate_on = pygame.image.load("Pictures/menu_pictures/big_button_plate_on.png").convert_alpha()
    
    running = True
    must_quit = False
    which_control = ""
    new_ship_name = ""
    player_name = ""
    dif = 0
    delete_account = False
    draw_mouse = True
    how_many_button = 0
    mouse_1 = pygame.mouse.get_pos()
    enter = False

    mouse_form = pygame.draw.circle(context.screen, (255, 255, 255), pygame.mouse.get_pos(), 10)

    while running:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                must_quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            mouse_click = True
        if not draw_mouse:
            mouse_2 = pygame.mouse.get_pos()
            if not mouse_1 == mouse_2:
                draw_mouse = True
                how_many_button = 0
        mouse_press_time = mouse_press_time + 1
        keys = pygame.key.get_pressed()

        context.screen.fill((0, 0, 0))

        if which_menu == "main menu":

            if keys[options_save.up_control] and mouse_press_time > 15:
                mouse_1 = pygame.mouse.get_pos()
                mouse_press_time = 0
                draw_mouse = False
                how_many_button = how_many_button - 1
                if how_many_button <= 0:
                    how_many_button = 1
            if keys[options_save.down_control] and mouse_press_time > 15:
                mouse_1 = pygame.mouse.get_pos()
                mouse_press_time = 0
                draw_mouse = False
                how_many_button = how_many_button + 1
                if how_many_button > 4:
                    how_many_button = 4
            if keys[pygame.K_RETURN]:
                enter = True
            else:
                enter = False

            print_text("SpaceWar", 120, (0, 0, 255), ((1280 / 2), 100), context)
            print_text("Alpha 0.2.", 45, (255, 255, 255), ((1280 / 3 * 2), 150), context)
            play_game = context.screen.blit(button_plate, ((1280 / 2 - 100), 160))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["play"], 45, (255, 255, 255), ((1280 / 2 + 15), 240), context)
            else:
                print_text((options_save.languages[options_save.select_language])["continue"], 45, (255, 255, 255), ((1280 / 2 + 15), 240), context)
            credits = context.screen.blit(button_plate, ((1280 / 2 - 100), 305))
            print_text((options_save.languages[options_save.select_language])["credits"], 45, (255, 255, 255), ((1280 / 2 + 15), 385), context)
            options = context.screen.blit(button_plate, ((1280 / 2 - 100), 450)) 
            print_text((options_save.languages[options_save.select_language])["options"], 45, (255, 255, 255), ((1280 / 2 + 15), 530), context)
            game_quit = context.screen.blit(button_plate, ((1280 / 2 - 100), 595))
            if not escape:
                print_text((options_save.languages[options_save.select_language])["quit"], 45, (255, 255, 255), ((1280 / 2 + 15), 675), context)
            else:
                print_text((options_save.languages[options_save.select_language])["finish"], 45, (255, 255, 255), ((1280 / 2 + 15), 675), context)

            if (play_game.colliderect(mouse_form) and draw_mouse) or how_many_button == 1:
                context.screen.blit(button_plate_on, ((1280 / 2 - 100), 160))
                if not escape:
                    print_text((options_save.languages[options_save.select_language])["play"], 45, (255, 255, 255), ((1280 / 2 + 20), 245), context)
                else:
                    print_text((options_save.languages[options_save.select_language])["continue"], 45, (255, 255, 255), ((1280 / 2 + 20), 245), context)
            if (credits.colliderect(mouse_form) and draw_mouse) or how_many_button == 2:
                context.screen.blit(button_plate_on, ((1280 / 2 - 100), 305))
                print_text((options_save.languages[options_save.select_language])["credits"], 45, (255, 255, 255), ((1280 / 2 + 20), 390), context)
            if (options.colliderect(mouse_form) and draw_mouse) or how_many_button == 3:
                context.screen.blit(button_plate_on, ((1280 / 2 - 100), 450))
                print_text((options_save.languages[options_save.select_language])["options"], 45, (255, 255, 255), ((1280 / 2 + 20), 535), context)
            if (game_quit.colliderect(mouse_form) and draw_mouse) or how_many_button == 4:
                context.screen.blit(button_plate_on, ((1280 / 2 - 100), 595))
                if not escape:
                    print_text((options_save.languages[options_save.select_language])["quit"], 45, (255, 255, 255), ((1280 / 2 + 20), 680), context)
                else:
                    print_text((options_save.languages[options_save.select_language])["finish"], 45, (255, 255, 255), ((1280 / 2 + 20), 680), context)
            if (play_game.colliderect(mouse_form) and mouse_click and draw_mouse) or (how_many_button == 1 and enter and mouse_press_time > 15) or keys[pygame.K_ESCAPE]:
                if not escape and not keys[pygame.K_ESCAPE]:
                    mouse_press_time = 0
                    which_menu = "players"
                    delete_account = False
                    mouse_click = False
                    ic2 = False
                if escape:
                    return False
            if (credits.colliderect(mouse_form) and mouse_click and draw_mouse) or (how_many_button == 2 and enter):
                which_menu = "credits"
                credits_y = 720
            if (options.colliderect(mouse_form) and mouse_click and draw_mouse and mouse_press_time > 15) or (how_many_button == 3 and enter):
                mouse_press_time = 0
                how_many_button = 1
                which_menu = "options"
            if (game_quit.colliderect(mouse_form) and mouse_click and draw_mouse and mouse_press_time > 15) or (how_many_button == 4 and enter):
                mouse_press_time = 0
                if not escape:
                    running = False
                    must_quit = True
                else:
                    return True, None

        if which_menu == "options":

            if keys[options_save.up_control] and mouse_press_time > 15:
                mouse_1 = pygame.mouse.get_pos()
                mouse_press_time = 0
                draw_mouse = False
                how_many_button = how_many_button - 1
                if how_many_button <= 0:
                    how_many_button = 1
            if keys[options_save.down_control] and mouse_press_time > 15:
                mouse_1 = pygame.mouse.get_pos()
                mouse_press_time = 0
                draw_mouse = False
                how_many_button = how_many_button + 1
                if how_many_button > 3:
                    how_many_button = 3
            if keys[pygame.K_RETURN]:
                enter = True
            else:
                enter = False

            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            game_options_button = context.screen.blit(button_plate, (context.width / 2 - 110, 140))
            print_text((options_save.languages[options_save.select_language])["game"], 45, (255, 255, 255), ((1280 / 2 + 5), 220), context)
            controls_button = context.screen.blit(button_plate, (context.width / 2 - 110, 285))
            print_text((options_save.languages[options_save.select_language])["controls"], 45, (255, 255, 255), ((1280 / 2 + 5), 365), context)
            back_main_menu = context.screen.blit(button_plate, (context.width / 2 - 110, 510))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 5), 590), context)

            if (game_options_button.colliderect(mouse_form) and draw_mouse) or (how_many_button == 1 and not draw_mouse):
                context.screen.blit(button_plate_on, (context.width / 2 - 110, 140))
                print_text((options_save.languages[options_save.select_language])["game"], 45, (255, 255, 255), ((1280 / 2 + 10), 225), context)
            if (controls_button.colliderect(mouse_form) and draw_mouse) or (how_many_button == 2 and not draw_mouse):
                context.screen.blit(button_plate_on, (context.width / 2 - 110, 285))
                print_text((options_save.languages[options_save.select_language])["controls"], 45, (255, 255, 255), ((1280 / 2 + 10), 370), context)
            if (back_main_menu.colliderect(mouse_form) and draw_mouse) or (how_many_button == 3 and not draw_mouse):
                context.screen.blit(button_plate_on, (context.width / 2 - 110, 510))
                print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 10), 595), context)
            if (back_main_menu.colliderect(mouse_form) and mouse_click and mouse_press_time >= 15 and draw_mouse) or (keys[pygame.K_ESCAPE] and mouse_press_time > 15) or (how_many_button == 3 and not draw_mouse and enter):
                mouse_press_time = 0
                if not draw_mouse:
                    how_many_button = 1
                which_menu = "main menu"
            if (game_options_button.colliderect(mouse_form) and mouse_click and draw_mouse) or (how_many_button == 1 and not draw_mouse and enter and mouse_press_time > 15):
                mouse_press_time = 0
                if not draw_mouse:
                    how_many_button = 1
                which_menu = "game options"
            if (controls_button.colliderect(mouse_form) and mouse_click and draw_mouse) or (how_many_button == 2 and not draw_mouse and enter):
                mouse_press_time = 0
                if not draw_mouse:
                    how_many_button = 1
                which_menu = "controls"
                get_input = False

        if which_menu == "game options":
            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            print_text((options_save.languages[options_save.select_language])["language"], 45, (255, 255, 255), ((1280 / 3), 150), context)
            print_text((options_save.languages[options_save.select_language])["fullscreen"], 45, (255, 255, 255), ((1280 / 3), 250), context)
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
            back_main_menu = context.screen.blit(button_plate, (530, 510))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 5), 590), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(button_plate_on, (530, 510))
                print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 10), 595), context)

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
            if (back_main_menu.colliderect(mouse_form) and mouse_click) or keys[pygame.K_ESCAPE]:
                mouse_press_time = 0
                which_menu = "options"
                options_save.saving_writing()

        if which_menu == "controls":
            print_text((options_save.languages[options_save.select_language])["options"], 70, (255, 255, 255), ((1280 / 2), 60), context)
            back_main_menu = context.screen.blit(button_plate, (context.width / 2 - 110, 510))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 5), 590), context)
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
                    context.screen.blit(button_plate_on, (context.width / 2 - 110, 510))
                    print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 10), 595), context)

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
                if (back_main_menu.colliderect(mouse_form) and mouse_click) or keys[pygame.K_ESCAPE]:
                    mouse_press_time = 0
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
                context.screen.blit(credits_eng, (0, credits_y))
            else:
                context.screen.blit(credits_hun, (0, credits_y))

            credits_y = credits_y - 1
            if keys[pygame.K_ESCAPE] or credits_y <= -1050:
                which_menu = "main menu"

        if which_menu == "players":
            if not os.path.isdir("texts/players"):
                os.mkdir("texts/players")
            players = os.listdir("texts/players")
            how_many = 1
            how_many_2 = 1
            print_text((options_save.languages[options_save.select_language])["players"], 80, (255, 255, 255), ((1280 / 2), 100), context)

            if ic2:
                print_text((options_save.languages[options_save.select_language])["max ships"], 60, (255, 255, 255), ((1280 / 2), context.height / 2 + 20), context)

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
                if player_box.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                    mouse_press_time = 0
                    unlock_player_name = player_name
                    if not delete_account:
                        if not escape:
                            mau = Map_and_Upgrades(player_name)
                            which_menu = "map"
                        else:
                            return False, player_name
                    else:
                        os.remove(f"texts/players/{player_name}")
                        delete_account = False

            new_ship = context.screen.blit(big_button_plate, ((context.width / 5 - 200), 575))
            print_text((options_save.languages[options_save.select_language])["create"], 45, (255, 255, 255), ((context.width / 5 + 25), 665), context)
            delete_ship = context.screen.blit(big_button_plate, ((context.width / 5 + 275), 575))
            if delete_account == False:
                print_text((options_save.languages[options_save.select_language])["delete"], 45, (255, 255, 255), ((context.width / 5 * 3 - 10), 665), context)
            else:
                print_text((options_save.languages[options_save.select_language])["cancel"], 45, (255, 255, 255), ((context.width / 5 * 3 - 10), 665), context)
            back_main_menu = context.screen.blit(button_plate, (context.width / 4 * 3 + 60, 590))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 175), 670), context)
            
            if new_ship.colliderect(mouse_form):
                context.screen.blit(big_button_plate_on, ((context.width / 5 - 195), 580))
                print_text((options_save.languages[options_save.select_language])["create"], 45, (255, 255, 255), ((context.width / 5 + 25), 663), context)
            if delete_ship.colliderect(mouse_form):
                context.screen.blit(big_button_plate_on, ((context.width / 5 + 275), 580))
                if delete_account == False:
                    print_text((options_save.languages[options_save.select_language])["delete"], 45, (255, 255, 255), ((context.width / 5 * 3 - 10), 662), context)
                else:
                    print_text((options_save.languages[options_save.select_language])["cancel"], 45, (255, 255, 255), ((context.width / 5 * 3 - 10), 662), context)
            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(button_plate_on, (context.width / 4 * 3 + 60, 590))
                print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 675), context)

            if new_ship.colliderect(mouse_form) and mouse_click:
                hms = 0
                for ns_hm in os.listdir("texts/players"):
                    hms = hms + 1
                if 6 > hms:
                    delete_account = False
                    which_menu = "new ship"
                    new_ship_name = ""
                    dif = 0
                    get_key = False
                    ic = True
                else:
                    ic2 = True
            if delete_ship.colliderect(mouse_form) and mouse_click and mouse_press_time >= 15:
                if delete_account:
                    delete_account = False
                else:
                    delete_account = True
                mouse_press_time = 0
            if (back_main_menu.colliderect(mouse_form) and mouse_click) or (keys[pygame.K_ESCAPE] and mouse_press_time > 15):
                mouse_press_time = 0
                which_menu = "main menu"

        if which_menu == "new ship":
            print_text((options_save.languages[options_save.select_language])["create"], 80, (255, 255, 255), ((1280 / 2), 100), context)
            name_button = pygame.draw.rect(context.screen, (255, 255, 0), ((context.width // 3 * 2 - 100), context.height // 3 - 40, 200, 80))
            back_main_menu = context.screen.blit(button_plate, (context.width / 2 + 175, 525))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 290), 605), context)
            print_text((options_save.languages[options_save.select_language])["ship name"], 45, (255, 255, 255), ((context.width // 3), context.height // 3), context)
            print_text((options_save.languages[options_save.select_language])["difficulty"], 45, (255, 255, 255), ((1280 / 3), 350), context)
            difficulty_button = pygame.draw.rect(context.screen, (255, 255, 255), ((1280 / 3 * 2 - 75), 325, 150, 50))
            create_button = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 - 100), 550, 200, 80))
            print_text((options_save.languages[options_save.select_language])["create2"], 45, (0, 0, 0), ((context.width / 4), 590), context)

            if not ic:
                print_text((options_save.languages[options_save.select_language])["bad name"], 60, (255, 255, 255), ((context.width / 2), 590), context)

            if dif == 1:
                d = (options_save.languages[options_save.select_language])["hard"]
            if dif == 0:
                d = (options_save.languages[options_save.select_language])["normal"]
            if dif == -1:
                d = (options_save.languages[options_save.select_language])["easy"]
            print_text(d, 45, (0, 0, 0), ((1280 / 3 * 2), 350), context)

            if back_main_menu.colliderect(mouse_form):
                context.screen.blit(button_plate_on, (context.width / 2 + 175, 525))
                print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 2 + 295), 610), context)
            if create_button.colliderect(mouse_form):
                context.screen.blit(ship, ((context.width / 4 - 165), 550))
            if name_button.colliderect(mouse_form) and mouse_click:
                get_key = True
            if (back_main_menu.colliderect(mouse_form) and mouse_click) or keys[pygame.K_ESCAPE]:
                mouse_press_time = 0
                which_menu = "players"
                delete_account = False
            if difficulty_button.colliderect(mouse_form) and mouse_click and mouse_press_time > 15:
                dif = dif + 1
                mouse_press_time = 0
                if dif >= 2:
                    dif = -1
            if create_button.colliderect(mouse_form) and mouse_click:
                mouse_press_time = 0
                if not new_ship_name == "":
                    ic = True
                    for ship_name in os.listdir("texts/players"):
                        if ship_name == new_ship_name:
                            ic = False
                    if ic:
                        with open(f"texts/players/{new_ship_name}", "w") as f:
                            f.write(f"{dif}\n")
                            f.write("1\n")
                            f.write("1\n")
                            f.write("0\n")
                            f.write("0\n")
                            f.write("1\n")
                            f.write("1\n")
                            f.write("0\n")
                            f.write("0\n")
                            f.write("0\n")
                        mau = Map_and_Upgrades(new_ship_name)
                        which_menu = "map"
                        ic2 = False
                else:
                    ic = False

            if get_key:
                typing = True
                while typing:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            if event.unicode == chr(pygame.K_ESCAPE) or event.unicode == chr(pygame.K_BACKSPACE) or event.unicode == chr(pygame.K_RETURN):
                                if event.unicode == chr(pygame.K_BACKSPACE):
                                    if len(new_ship_name) > 0:
                                        new_ship_name = new_ship_name[:-1]
                                else:
                                    get_key = False
                                typing = False
                            else:
                                typing = False
                                new_ship_name = new_ship_name + event.unicode
            print_text(new_ship_name, 45, (255, 255, 255), (context.width // 3 * 2, context.height // 3), context)

        if which_menu == "map":
            which_menu, mouse_press_time = mau.map(context, mouse_form, mouse_click, mouse_press_time, options_save, ship)
            if which_menu == "play the game":
                return False, unlock_player_name

        if which_menu == "upgrade":
            which_menu, mouse_press_time = mau.upgrade(context, mouse_form, mouse_click, mouse_press_time, options_save, ship)
            if which_menu == "play the game":
                return False, unlock_player_name
        if draw_mouse:
            mouse_form = pygame.draw.circle(context.screen, (255, 255, 255), pygame.mouse.get_pos(), 10)

        pygame.display.flip()
        context.delta_time = context.clock.tick(60) / 1000

    return must_quit, None
