import pygame
import numpy as np

from .framework import GameBase
from .config import config
from .background import ScrollingStars
from .ship import Ship
from .objects import Planet, FloatText





class NotRocketScience(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size))
        
        self.star_background = ScrollingStars(
            tuple(5 * dim for dim in self.screen_size),
            self.screen_size,
            0.5 * np.array(self.screen_size),
            n_stars=1000,
            spacecolor=config.hex_to_rgb(config.space_color),
            starcolor=config.hex_to_rgb(config.star_color),
            n_layers=4
        )
        
        self.txt = FloatText()
        self.ship = Ship()
        
        # self.planets = [Planet(np.array((900, 200)))]

        self.n_planets = config.number_of_planets
        self.planet_initial_positions = np.hstack((
            np.random.randint(-10 * self.screen_size[0] / 2, 10 * self.screen_size[0] / 2, size=(self.n_planets, 1)),
            np.random.randint(-10 * self.screen_size[1] / 2, 10 * self.screen_size[1] / 2, size=(self.n_planets, 1))
        ))
        self.planets = [Planet(pos) for pos in self.planet_initial_positions]

        self.pos = 0.5 * np.array(self.screen_size)
        self.coordinates = self.pos
        self.speed = np.array([0, 0])
        self.damp = config.movement_damping

    @property
    def screen_coordinates(self):
        self.coordinates = self.coordinates + self.frametime_s * self.speed
        return tuple(int(c / s) for c, s in zip(self.coordinates, self.screen_size))
    
    def render_scene(self):
        self.ship.apply_rotation()

        gravs = np.vstack([p.calc_gravity(self.pos) for p in self.planets])
        grav_accel = np.sum(gravs, axis=0)

        self.speed = self.speed + self.frametime_s * (self.ship.calc_acceleration() - grav_accel - self.speed * self.damp)
        # self.logger.debug(self.screen_coordinates)

        self.star_background.blit(self.screen, self.frametime_s, self.speed)
        [p.update_position_and_draw(self.screen, self.frametime_s, self.speed) for p in self.planets]
        self.ship.draw(self.screen, self.pos)

        self.txt.render(
            self.screen,
            (self.screen_width / 2, 0),
            f"coordinates: ({self.coordinates[0]:5.0f},{self.coordinates[1]:5.0f}) screen_coordinates: {self.screen_coordinates} speed: ({self.speed[0]:5.0f},{self.speed[1]:5.0f})"
        )

    def process_inputs(self):
        self.ship.controls()