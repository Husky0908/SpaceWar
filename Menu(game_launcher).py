import pygame
from SpaceWar import main

def menu(esc):
    menu_screen = pygame.display.set_mode((1280, 720))
    menu_clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

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
        play_game = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 2 - 100), 200, 200, 80))
        game_quit = pygame.draw.rect(menu_screen, (255, 255, 255), ((1280 / 2 - 100), 400, 200, 80))

        if play_game.colliderect(mouse_form) and mouse_click:
            main()
        if game_quit.colliderect(mouse_form) and mouse_click:
            running = False

        pygame.display.flip()
        menu_clock.tick(60)

menu(False)
