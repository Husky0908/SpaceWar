import pygame
from SpaceWar import main

def menu(esc):
    menu_screen = pygame.display.set_mode((1280, 720))
    menu_clock = pygame.time.Clock()

    which_menu = "main menu"

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    play_button = pygame.image.load("Pictures/menu_pictures/playbutton.png").convert_alpha()
    options_button = pygame.image.load("Pictures/menu_pictures/optionsbutton.png").convert_alpha()
    exit_button = pygame.image.load("Pictures/menu_pictures/exitbutton.png").convert_alpha()
    ship = pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha()
    options_controls = pygame.image.load("Pictures/menu_pictures/options_controls.png").convert_alpha()
    back_button = pygame.image.load("Pictures/menu_pictures/backbutton.png").convert_alpha()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            else:
                mouse_click = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and esc:
            return None

        menu_screen.fill((0, 0, 0))

        mouse_form = pygame.draw.circle(menu_screen, (255, 255, 255), pygame.mouse.get_pos(), 10)
        if which_menu == "main menu":
            play_game = menu_screen.blit(play_button, ((1280 / 2 - 100), 200, 200, 80))
            options = menu_screen.blit(options_button, ((1280 / 2 - 100), 325, 200, 80))
            game_quit = menu_screen.blit(exit_button, ((1280 / 2 - 100), 450, 200, 80))

            if play_game.colliderect(mouse_form):
                menu_screen.blit(ship,((1280 / 2 - 165), 200))
            if options.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 325))
            if game_quit.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 450))
            if play_game.colliderect(mouse_form) and mouse_click:
                main()
            if options.colliderect(mouse_form) and mouse_click:
                which_menu = "options"
            if game_quit.colliderect(mouse_form) and mouse_click:
                running = False

        if which_menu == "options":
            menu_screen.blit(options_controls, (330, 100))
            back_main_menu = menu_screen.blit(back_button, (540, 550))

            if back_main_menu.colliderect(mouse_form):
                menu_screen.blit(ship, ((1280 / 2 - 165), 550))
            if back_main_menu.colliderect(mouse_form) and mouse_click:
                which_menu = "main menu"

        pygame.display.flip()
        menu_clock.tick(60)

    pygame.quit()

menu(False)
