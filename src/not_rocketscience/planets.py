import pygame
import numpy as np
from .config import config
import logging
from .math import deriv_combination, newton_gravity
from scipy.spatial import KDTree


class PlanetGroup:

    def __init__(self, planet_class, coordinates, diameter_min=20, diameter_max=180):
        self.planets = [
            planet_class(pos, diameter=np.random.randint(diameter_min, diameter_max))
            for pos in coordinates
        ]
        self.tree = KDTree(coordinates)

    def nearest_neighbour_distances_slow(self, coordinate, max_dist):
        planet_indices = [
            index for index, p in enumerate(self.planets) if np.abs(p.coordinates - coordinate).sum() < max_dist
        ]

        if len(planet_indices):
            diffs = np.vstack([self.planets[i].coordinates for i in planet_indices]) - coordinate
            diffs_norms = np.sqrt(np.sum(diffs**2, axis=1))
        else:
            diffs, diffs_norms = np.array([]), np.array([])
        return diffs, diffs_norms, planet_indices 
    
    def nearest_neighbour_distances(self, coordinate, max_dist):
        diffs_norms, planet_indices = self.tree.query(coordinate, len(self.planets), distance_upper_bound=max_dist)
        diffs_norms = diffs_norms[planet_indices < len(self.planets)]
        planet_indices = planet_indices[planet_indices < len(self.planets)]

        if len(planet_indices):
            diffs = np.vstack([self.planets[i].coordinates for i in planet_indices]) - coordinate
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


class BasePlanet:
    def __init__(self, position, diameter=50):
        self.logger = logging.getLogger("Planet")
        self.render_range = 200
        self.diameter = diameter
        self.grav_force = deriv_combination(4, 6, 0.2, 4, 1.2)
        self.scale = (self.diameter + 25) / 0.15
        self.pos = position
        self.coordinates = position

    @property
    def surface(self):
        raise NotImplementedError("needs to be implemented in subclass")
    
    def calc_gravity(self, diff, dist):
        return self.grav_force(dist / self.scale) * diff / dist
    
    def update_position_and_draw(self, screen, dt, speed):
        self.pos = self.pos - dt * speed
        if self.pos[0] > -self.render_range and self.pos[1] < screen.get_width() + self.render_range \
            and self.pos[1] > -self.render_range and self.pos[1] < screen.get_height() + self.render_range:
            screen.blit(self.surface, self.surface.get_rect(center=tuple(self.pos)))


class PlanetSimple(BasePlanet):

    def __init__(self, position, diameter=50):
        super().__init__(position, diameter=diameter)
        self.color = (np.random.randint(low=150, high=255), np.random.randint(low=50, high=220)) + (0,)
        self._surface = pygame.Surface((self.diameter, self.diameter)).convert_alpha()
        self._surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self._surface, self.color + (100,), (0, 0, self.diameter, self.diameter))
        pygame.draw.ellipse(self._surface, self.color + (255,), (0.1 * self.diameter, 0.1 * self.diameter, self.diameter * 0.8, self.diameter * 0.8))
        self.logger.info(f"Created Planet at {tuple(self.pos)} with color {config.rgb_to_hex(self.color)}")
    
    @property
    def surface(self):
        return self._surface
    
    

    



        