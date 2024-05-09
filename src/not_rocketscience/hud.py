import pygame
from .config import config

class FloatText:

    def __init__(self, font="consolas", fontsize=15):
        pygame.font.init()
        self.font = pygame.font.SysFont(font, fontsize)
        
    def render(self, screen, pos, text):
        text_surf = self.font.render(text, False, config.star_color, config.space_color)
        screen.blit(text_surf, text_surf.get_rect(midtop=pos))