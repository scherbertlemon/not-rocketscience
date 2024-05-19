import pygame
from .config import config

class FloatText:

    def __init__(self, font="consolas", fontsize=15):
        pygame.font.init()
        self.font = pygame.font.SysFont(font, fontsize)
        
    def render(self, screen, pos, text):
        text_surf = self.font.render(text, False, config.star_color, config.space_color)
        screen.blit(text_surf, text_surf.get_rect(midtop=pos))


class FuelGaige:

    def __init__(self, screen_position, width=300):
        self.width = width
        self.height = 13
        self.fill_height = 5 
        self.surface = pygame.Surface((self.width, self.height))
        self.screen_position = screen_position
        self.bg_color = config.hex_to_rgb(config.red_color)
        self.fg_color = config.hex_to_rgb(config.fire_color)

    def draw(self, screen, full_amount):
        self.surface.fill(self.bg_color)
        filled = int(full_amount * self.width)
        pygame.draw.rect(self.surface, self.fg_color, (0, self.fill_height, filled, self.height - self.fill_height))
        screen.blit(self.surface, self.surface.get_rect(topleft=self.screen_position))
    
