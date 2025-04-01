import pygame
from base.context import PygameContext

def print_text(text, size, color, x_y, context: PygameContext):
    text_1 = pygame.font.Font(None, size)
    text_2 = text_1.render(text, True, color)
    text_3 = text_2.get_rect(center=x_y)
    context.screen.blit(text_2, text_3)