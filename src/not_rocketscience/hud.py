import pygame
from .config import config


class FloatText:

    def __init__(self, font="PT Mono", fontsize=15):
        pygame.font.init()
        self.fs = fontsize
        self.font = pygame.font.SysFont(font, fontsize)
        
    def render(self, screen, pos, text):
        text_surf = self.font.render(text, False, config.colors.stars, config.colors.space)
        screen.blit(text_surf, text_surf.get_rect(midtop=pos))


class PilotDisplay(FloatText):

    def __init__(self, screen_position_top_right, font="PT Mono", fontsize=30) -> None:
        super().__init__(font=font, fontsize=fontsize)
        self.screen_position = screen_position_top_right

    def render(self, screen, picture, name):
        rect = picture.get_rect(topright=self.screen_position)
        screen.blit(picture, rect)
        screen.blit(self.font.render(name, False, config.colors.stars), rect.bottomleft)


class FuelGaige:

    def __init__(self, screen_position_bottom_left, width=300):
        self.width = width
        self.height = 13
        self.fill_height = 5 
        self.surface = pygame.Surface((self.width, self.height))
        self.screen_position = screen_position_bottom_left
        self.bg_color = config.colors.hud_red
        self.fg_color = config.colors.fire

    def draw(self, screen, full_amount):
        self.surface.fill(self.bg_color)
        filled = int(full_amount * self.width)
        pygame.draw.rect(self.surface, self.fg_color, (0, self.fill_height, filled, self.height - self.fill_height))
        screen.blit(self.surface, self.surface.get_rect(bottomleft=self.screen_position))
    
