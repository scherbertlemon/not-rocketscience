import pygame
import numpy as np

from .framework import GameBase
from .config import config
from .background import LayeredScrollingStarBackground
from .ship import Ship
from .planets import PlanetSimple, PlanetGroup, PlanetTexture
from .hud import FloatText

from time import time



class NotRocketScience(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size), fps=config.fps)
        
        self.star_background = LayeredScrollingStarBackground(
            tuple(dim * 2 for dim in self.screen_size),
            0.5 * np.array(self.screen_size),
            n_stars=config.background_number_of_stars,
            spacecolor=config.hex_to_rgb(config.space_color),
            starcolor=config.hex_to_rgb(config.star_color),
            n_layers=config.background_number_of_layers
        )
        
        self.txt = FloatText(fontsize=12)
        self.ship = Ship(0.5 * np.array(self.screen_size))

        self.n_planets = config.number_of_planets
        self.planets = PlanetGroup(
            PlanetTexture,
            np.hstack((
                np.random.randint(-10 * self.screen_size[0], 10 * self.screen_size[0], size=(self.n_planets, 1)),
                np.random.randint(-10 * self.screen_size[1], 10 * self.screen_size[1], size=(self.n_planets, 1))
            )),
            diameter_max=150,
            diameter_min=10,
            planet_kwargs=dict(rotation_speed=(20, 50), atmosphere_thickness=10, atmosphere_layers=5)
        )

        self.speed = np.array([0, 0])
        self.damp = config.movement_damping

    @property
    def screen_coordinates(self):
        return tuple(int(c / s) for c, s in zip(self.ship.coordinates, self.screen_size))
    
    def render_scene(self):

        # planets_in_block = [
        #     p for p in self.planets if np.abs(self.ship.coordinates - p.coordinates).sum() < self.screen_height + self.screen_width]
        # gravity_contrib = [p.calc_gravity(self.ship.pos) for p in planets_in_block] if planets_in_block else [np.zeros(2)]        
        # grav_accel= np.vstack(gravity_contrib).sum(axis=0)

        # s = time()
        grav_accel, planets_in_block = self.planets.calc_gravity_contrib(
            self.ship.coordinates,
            self.screen_height + self.screen_width
        )
        # self.logger.debug(f"grav comp: {time() - s}s")
        self.speed = self.speed + self.frametime_s * (self.ship.calc_acceleration() - grav_accel - self.speed * self.damp)
        # self.logger.debug(self.screen_coordinates)

        self.star_background.draw_tiles(self.screen, self.ship.pos, self.frametime_s, self.speed)
        [p.update_position_and_draw(self.screen, self.frametime_s, self.speed) for p in self.planets.planets]
        
        self.ship.apply_rotation()
        self.ship.move(self.frametime_s * self.speed)
        self.ship.draw(self.screen)

        self.txt.render(
            self.screen,
            (self.screen_width / 2, 0),
            (
                f"coordinates: ({self.ship.coordinates[0]:5.0f},{self.ship.coordinates[1]:5.0f}) "
                f"screen_coordinates: {self.screen_coordinates} "
                f"speed: ({self.speed[0]:5.0f},{self.speed[1]:5.0f}) "
                f"feeling pull from planets: {len(planets_in_block)} "
                f"FPS: {self.clock.get_fps():3.0f}"
            )
        )

    def process_inputs(self):
        self.ship.controls()


def cli():
    game = NotRocketScience()
    game.gameloop()