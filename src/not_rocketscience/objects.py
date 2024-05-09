import pygame
import numpy as np
from .config import config
import logging
from .math import deriv_combination, newton_gravity


class Planet:

    def __init__(self, position, radius=50):
        self.logger = logging.getLogger("Planet")
        self.render_range = 200
        self.radius = radius
        self.grav_force = deriv_combination(4, 6, 0.2, 4, 1.2)
        self.scale = (self.radius + 25) / 0.15

        # self.scale = 300
        self.pos = position
        self.color = (np.random.randint(low=150, high=255), np.random.randint(low=50, high=220)) + (0,)
        self.surface = pygame.Surface((self.radius, self.radius)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.surface, self.color + (100,), (0, 0, self.radius, self.radius))
        pygame.draw.ellipse(self.surface, self.color + (255,), (0.1 * self.radius, 0.1 * self.radius, self.radius * 0.8, self.radius * 0.8))
        self.logger.info(f"Created Planet at {tuple(self.pos)} with color {config.rgb_to_hex(self.color)}")
        
    def calc_gravity(self, other_pos):
        diff = self.pos - other_pos
        diff_norm = np.sqrt(np.sum(diff**2))
        return self.grav_force(diff_norm / self.scale) * diff / diff_norm

    def update_position_and_draw(self, screen, dt, speed):
        self.pos = self.pos - dt * speed
        if self.pos[0] > -self.render_range and self.pos[1] < screen.get_width() + self.render_range \
            and self.pos[1] > -self.render_range and self.pos[1] < screen.get_height() + self.render_range:
            screen.blit(self.surface, self.surface.get_rect(center=tuple(self.pos)))


class FloatText:

    def __init__(self, font="consolas", fontsize=15):
        pygame.font.init()
        self.font = pygame.font.SysFont(font, fontsize)
        
    def render(self, screen, pos, text):
        text_surf = self.font.render(text, False, config.star_color, config.space_color)
        screen.blit(text_surf, text_surf.get_rect(midtop=pos))
        