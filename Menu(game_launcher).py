import pygame
from SpaceWar import main

def menu(esc):
    menu_screen = pygame.display.set_mode((1280, 720))
    menu_clock = pygame.time.Clock()

    which_menu = "main menu"

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    play_button = pygame.image.load("Pictures/menu_pictures/playbutton.png").convert_alpha()
    play_button_coll = pygame.image.load("Pictures/menu_pictures/playbuttoncolliderect.png").convert_alpha()
    options_button = pygame.image.load("Pictures/menu_pictures/playotions.png").convert_alpha()
    options_button_coll = pygame.image.load("Pictures/menu_pictures/playoptionscolliderect.png").convert_alpha()
    exit_button = pygame.image.load("Pictures/menu_pictures/playexit.png").convert_alpha()
    exit_button_coll = pygame.image.load("Pictures/menu_pictures/playexitcolliderect.png").convert_alpha()

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
                play_game = menu_screen.blit(play_button_coll, ((1280 / 2 - 142.5), 200, 200, 80))
            if options.colliderect(mouse_form):
                options = menu_screen.blit(options_button_coll, ((1280 / 2 - 142.5), 325, 200, 80))
            if game_quit.colliderect(mouse_form):
                game_quit = menu_screen.blit(exit_button_coll, ((1280 / 2 - 142.5), 450, 200, 80))
            if play_game.colliderect(mouse_form) and mouse_click:
                main()
            if options.colliderect(mouse_form) and mouse_click:
                which_menu = "options"
            if game_quit.colliderect(mouse_form) and mouse_click:
                running = False

        pygame.display.flip()
        menu_clock.tick(60)

    pygame.quit()

menu(False)
