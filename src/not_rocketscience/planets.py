"""
Takes care of planet animation and gravity calculation for all planets as a group
"""

import logging
import numpy as np
import pygame
from scipy.spatial import KDTree

from .config import config
from .math import (
    weird_gravity_force,
    weird_gravity_force_derivative,
    newton_gravity_force,
    newton_gravity_force_derivative,
    newton_iteration,
    canonical_weird_parameterset,
    canonical_newton_parameterset
)


class PlanetGroup:
    """
    Manages all planets in the game, especially for efficient gravity calculation. Planets can be
    instantiated with different Planet classes, which might have different appearance.

    :param planet_class: class to instantiate indivudal planets. Can be :py:class:`PlanetSimple`
        or :py:class:`PlanetTexture` at the moment.
    :param coordinates: amount of planets x 2 ``numpy.array`` with planet coordinates in pixels.
    :param diameter_min: diameters of planets are selected randomly. ``diameter_min`` is the
        minimal planet diameter in pixels
    :param diameter_max: diameters of planets are selected randomly. ``diameter_max`` is the
        maximal planet diameter in pixels
    :param planet_kwargs: additional keyword arguments for the ``planet_class`` constructor
    """

    def __init__(self, planet_class, coordinates,
                 diameter_min=20, diameter_max=180,
                 planet_kwargs=None):
        if planet_kwargs is None:
            planet_kwargs = dict()

        self.planets = [
            planet_class(
                pos,
                diameter=np.random.randint(diameter_min, diameter_max),
                **planet_kwargs
            ) for pos in coordinates
        ]
        self.tree = KDTree(coordinates)

    def nearest_neighbour_distances_slow(self, coordinate, max_dist):
        """
        Gives the distances to all planets relative to a given coordinatem that are smaller than
        a given maximal distance. This method always calculates the distance for all planets and
        is inefficient. It exists purely for demonstration purposes.

        :param coordinate: 1 x 2 ``numpy.array`` representing the coordinate towards which
            distances of planets should be calculated.
        :param max_dist: if a planet distance is larger than ``max_dist`` in city_block metric,
            the distance and planet will not be returned
        :returns: tuple of (n x 2 ``numpy.array`` of connecting vectors,
            n x 1 ``numpy.array`` of distances,
            list of associated planet indices referring to ``self.planets``)
        """
        planet_indices = [
            index
            for index, p in enumerate(self.planets)
            if np.abs(p.coordinates - coordinate).sum() < max_dist
        ]

        if len(planet_indices):
            diffs = np.vstack([self.planets[i].coordinates for i in planet_indices]) - coordinate
            diffs_norms = np.sqrt(np.sum(diffs**2, axis=1))
        else:
            diffs, diffs_norms = np.array([]), np.array([])

        return diffs, diffs_norms, planet_indices

    def nearest_neighbour_distances(self, coordinate, max_dist):
        """
        Gives the distances to maximal 5 planets relative to a given coordinatem that are smaller
        than a given maximal distance. Uses a KDTree to speed query those distances quickly

        :param coordinate: 1 x 2 ``numpy.array`` representing the coordinate towards which
            distances of planets should be calculated.
        :param max_dist: if a planet distance is larger than ``max_dist`` in city_block metric,
            the distance and planet will not be returned
        :returns: tuple of (n x 2 ``numpy.array`` of connecting vectors,
            n x 1 ``numpy.array`` of distances,
            list of associated planet indices referring to ``self.planets``)
        """
        diffs_norms, planet_indices = self.tree.query(coordinate, 5, distance_upper_bound=max_dist)
        diffs_norms = diffs_norms[planet_indices < len(self.planets)]
        planet_indices = planet_indices[planet_indices < len(self.planets)]

        if len(planet_indices):
            diffs = np.vstack([self.planets[i].coordinates for i in planet_indices]) - coordinate
        else:
            diffs, diffs_norms = np.array([]), np.array([])

        return diffs, diffs_norms, planet_indices

    def calc_gravity_contrib(self, coordinate, max_dist):
        """
        Calculates the accumulated gravity force vector from nearest planets that act at
        ``coordinate``.

        :param coordinate: 1 x 2 ``numpy.array`` representing the coordinate towards which
            distances of planets should be calculated.
        :param max_dist: if a planet distance is larger than ``max_dist`` in city_block metric,
            the distance and planet will not be returned
        :returns tuple of (1 x 2 gravity force vector, lis of contributing planet indices)
        """
        diffs, dists, planet_indices = self.nearest_neighbour_distances(coordinate, max_dist)
        gravity_contrib = [
            self.planets[index].calc_gravity(diff, diff_norm)
            for diff, diff_norm, index in zip(diffs, dists, planet_indices)
        ]
        gravity_contrib += [np.zeros(2)]  # in case empty
        return np.vstack(gravity_contrib).sum(axis=0), [self.planets[i] for i in planet_indices]

    def update_position_and_draw(self, screen, dt, speed):
        """
        Just a buld update method that calls the method of the same name for all planets.
        """
        for planet in self.planets:
            planet.update_position_and_draw(screen, dt, speed)


class BasePlanet:
    def __init__(self, position, diameter=50):
        self.logger = logging.getLogger("BasePlanet")
        self.render_range = 200
        self.diameter = diameter

        self.grav_force = weird_gravity_force(*canonical_weird_parameterset)
        self.scale = self.diameter / newton_iteration(weird_gravity_force(*canonical_weird_parameterset), weird_gravity_force_derivative(*canonical_weird_parameterset), 0, 0.001)
        
        # self.grav_force = newton_gravity_force(*canonical_newton_parameterset)
        # self.scale = 2 * self.diameter / newton_iteration(lambda r: newton_gravity_force(*canonical_newton_parameterset)(r) + 355, newton_gravity_force_derivative(*canonical_newton_parameterset), 0.03, 0.001)

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
            surf = self.surface
            screen.blit(surf, surf.get_rect(center=tuple(self.pos)))


class PlanetSimple(BasePlanet):

    def __init__(self, position, diameter=50, **kwargs):
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
    

class PlanetTexture(BasePlanet):
    def __init__(self, position, diameter=200, rotation_speed=100, atmosphere_thickness=20, atmosphere_layers=3):
        super().__init__(position, diameter=diameter)

        planet_texture_path = config.asset_path / "planets" / f"planet_{np.random.randint(1, 3):02d}.png"
        self.logger.info(f"Created planet with texture {planet_texture_path}")
        self.texture = pygame.image.load(planet_texture_path)
        new_width = self.diameter / self.texture.get_height() * self.texture.get_width()
        self.texture = pygame.transform.scale(self.texture, (new_width, self.diameter))

        self.atmos_color = self.texture.get_at(tuple(int(0.5 * s) for s in self.texture.get_size()))

        self._surface = pygame.Surface(2 * (self.diameter,)).convert_alpha()
        self._surface.fill((0, 0, 0, 0))
        
        self.last_time = pygame.time.get_ticks()
        
        if isinstance(rotation_speed, tuple):
            self.rotation_speed = np.random.randint(*rotation_speed)
        elif isinstance(rotation_speed, int):
            self.rotation_speed = rotation_speed
        else:
            raise NotImplementedError("rotation speed must be tuple(min, max) or an integer")
        
        self.texture_positions = [0, self.texture.get_width() + 1]

        self.atmoshpere_tickness, self._atmosphere = self.build_atmosphere(atmosphere_thickness, atmosphere_layers)

    def build_atmosphere(self, thickness, layers):
        base = pygame.Surface(2 * (self.diameter + 2 * thickness,)).convert_alpha()
        base.fill((0, 0, 0, 0))

        for i_layer in range(0, layers):
            pygame.draw.circle(
                base,
                self.atmos_color[:3] + (int((i_layer + 1) / layers * 255),),
                tuple(.5 * s for s in base.get_size()),
                0.5 * self.diameter + (1 - i_layer / layers) * thickness
            )

        return thickness, base

    @property
    def surface(self):
        now = pygame.time.get_ticks()
        timestep_s = (now - self.last_time) / 1000
        self.last_time = now

        pygame.draw.circle(self._surface, (255, 255, 255, 255), center=2 * (0.5 * self.diameter,), radius=0.5 * self.diameter)
        for pos in self.texture_positions:
            self._surface.blit(self.texture, (pos, 0), None, pygame.BLEND_RGBA_MULT)

        self._atmosphere.blit(self._surface, 2 * (self.atmoshpere_tickness,))  # this is slow
        self.texture_positions = [
            pos + (2 * self.texture.get_width() + 2 if pos < -self.texture.get_width() else 0) - timestep_s * self.rotation_speed
            for pos in self.texture_positions
        ]
        return self._atmosphere

    
    
    

    



        