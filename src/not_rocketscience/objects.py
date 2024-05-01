import pygame
import numpy as np
from .config import config
import logging


def exp2(b_2, s_2):
    def f(x):
        return np.exp(-b_2 * (x - s_2))
    return f


def ln(b_1, s_1):
    def f(x):
        return np.log(b_1 * (x + s_1))
    return f


def combination(A, b_1, s_1, b_2, s_2):
    def f(x):
        return A * ln(b_1, s_1)(x) * exp2(b_2, s_2)(x)
    return f


def deriv_combination(A, b_1, s_1, b_2, s_2):
    def f(x):
        return A * exp2(b_2, s_2)(x) * (1/(x + s_1) - b_2 * ln(b_1, s_1)(x))
    return f


def newton_gravity(r, min_r=0.2):
    return -100 / r**2 if r > min_r else -100 / min_r**2


class Planet:

    def __init__(self, position):
        self.logger = logging.getLogger("Planet")
        self.grav_force = deriv_combination(4, 6, 0.2, 4, 1.2)
        # self.grav_force = newton_gravity
        self.scale = 100 / 0.15

        # self.scale = 300
        self.pos = position
        self.color = tuple(np.random.randint(low=0, high=255, size=3))
        self.surface = pygame.Surface((50, 50)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.surface, self.color + (100,), (0, 0, 50, 50))
        pygame.draw.ellipse(self.surface, self.color + (255,), (5, 5, 40, 40))
        self.logger.info(f"Created Planet at {tuple(self.pos)} with color {config.rgb_to_hex(self.color)}")
        
    def calc_gravity(self, other_pos):
        diff = self.pos - other_pos
        diff_norm = np.sqrt(np.sum(diff**2))
        return self.grav_force(diff_norm / self.scale) * diff / diff_norm

    def update_position_and_draw(self, screen, dt, speed):
        self.pos = self.pos - dt * speed
        screen.blit(self.surface, self.surface.get_rect(center=tuple(self.pos)))


class FloatText:

    def __init__(self, font="consolas", fontsize=15):
        pygame.font.init()
        self.font = pygame.font.SysFont(font, fontsize)
        
    def render(self, screen, pos, text):
        text_surf = self.font.render(text, False, config.star_color, config.space_color)
        screen.blit(text_surf, text_surf.get_rect(midtop=pos))
        