import pygame
import numpy as np
from .config import config
import logging
from .math import deriv_combination, newton_gravity
from scipy.spatial import KDTree


class PlanetGroup:

    def __init__(self, coordinates, radius_min=20, radius_max=180):
        self.planets = [
            Planet(pos, radius=np.random.randint(radius_min, radius_max))
            for pos in coordinates
        ]
        self.tree = KDTree(coordinates)

    def nearest_neighbour_distances(self, coordinate, max_dist):
        diffs_norms, planet_indices = self.tree.query(coordinate, len(self.planets), distance_upper_bound=max_dist)
        diffs_norms = diffs_norms[planet_indices < len(self.planets)]
        planet_indices = planet_indices[planet_indices < len(self.planets)]
        
        # planet_indices = [
        #     index for index, p in enumerate(self.planets) if np.abs(p.coordinates - coordinate).sum() < max_dist
        # ]

        if len(planet_indices):
            diffs = np.vstack([self.planets[i].coordinates for i in planet_indices]) - coordinate
            diffs_norms = np.sqrt(np.sum(diffs**2, axis=1))
        else:
            diffs, diffs_norms = np.array([]), np.array([])
        return diffs, diffs_norms, planet_indices 
    
    def calc_gravity_contrib(self, coordinate, max_dist):
        diffs, dists, planet_indices = self.nearest_neighbour_distances(coordinate, max_dist)
        gravity_contrib = [
            self.planets[index].calc_gravity(diff, diff_norm)
            for diff, diff_norm, index in zip(diffs, dists, planet_indices)
        ]
        gravity_contrib += [np.zeros(2)]  # in case empty
        return np.vstack(gravity_contrib).sum(axis=0), [self.planets[i] for i in planet_indices]


class Planet:

    def __init__(self, position, radius=50):
        self.logger = logging.getLogger("Planet")
        self.render_range = 200
        self.radius = radius
        self.grav_force = deriv_combination(4, 6, 0.2, 4, 1.2)
        self.scale = (self.radius + 25) / 0.15

        # self.scale = 300
        self.pos = position
        self.coordinates = position
        self.color = (np.random.randint(low=150, high=255), np.random.randint(low=50, high=220)) + (0,)
        self.surface = pygame.Surface((self.radius, self.radius)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.surface, self.color + (100,), (0, 0, self.radius, self.radius))
        pygame.draw.ellipse(self.surface, self.color + (255,), (0.1 * self.radius, 0.1 * self.radius, self.radius * 0.8, self.radius * 0.8))
        self.logger.info(f"Created Planet at {tuple(self.pos)} with color {config.rgb_to_hex(self.color)}")
        
    def calc_gravity(self, diff, dist):
        # diff = self.pos - other_pos
        # diff_norm = np.sqrt(np.sum(diff**2))
        return self.grav_force(dist / self.scale) * diff / dist

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
        