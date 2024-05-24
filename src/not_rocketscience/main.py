"""
Defines the main game class
"""
import numpy as np
from .framework import GameBase
from .config import config
from .background import LayeredScrollingStarBackground
from .ship import Ship
from .planets import PlanetGroup, PlanetTexture
from .hud import FloatText, FuelGaige, PilotDisplay


class NotRocketScience(GameBase):
    """
    Main game class
    """
    def __init__(self):
        super().__init__(
            config.convert_tuple(config.screen_size),
            fps=config.fps,
            vsync=config.vsync
        )

        self.star_background = LayeredScrollingStarBackground(
            tuple(dim * 2 for dim in self.screen_size),
            0.5 * np.array(self.screen_size),
            n_stars=config.background_number_of_stars,
            spacecolor=config.hex_to_rgb(config.space_color),
            starcolor=config.hex_to_rgb(config.star_color),
            n_layers=config.background_number_of_layers
        )
        self.txt = FloatText(fontsize=12)
        self.fuel_gaige = FuelGaige((10, self.screen_height - 10))
        self.ship = Ship(
            0.5 * np.array(self.screen_size),
            **config.pilots[0]
        )
        self.pilot_display = PilotDisplay((self.screen_width - 10, 10), fontsize=20)

        self.n_planets = config.number_of_planets
        self.planets = PlanetGroup(
            PlanetTexture,
            np.hstack((
                np.random.randint(-30 * self.screen_size[0], 30 * self.screen_size[0], size=(self.n_planets, 1)),
                np.random.randint(-30 * self.screen_size[1], 30 * self.screen_size[1], size=(self.n_planets, 1))
            )),
            diameter_max=175,
            diameter_min=50,
            planet_kwargs=dict(rotation_speed=(20, 50), atmosphere_thickness=10, atmosphere_layers=5)
        )

        self.speed = np.array([0, 0])

    @property
    def screen_coordinates(self):
        return tuple(int(c / s) for c, s in zip(self.ship.world_coordinates, self.screen_size))
    
    def render_scene(self):

        grav_accel, planets_in_block = self.planets.calc_gravity_contrib(
            self.ship.world_coordinates,
            self.screen_height + self.screen_width
        )

        self.speed = self.speed + self.frametime_s * (
            self.ship.calc_acceleration() - grav_accel - self.speed * self.ship.ship_movement_damping
        )

        self.star_background.draw_tiles(self.screen, self.ship._screen_coordinates, self.frametime_s, self.speed)
        [p.update_position_and_draw(self.screen, self.frametime_s, self.speed) for p in self.planets.planets]
        
        self.ship.regenerate_fuel(
            self.frametime_s,
            1.0  # np.sqrt(np.sum(grav_accel**2)) * 5 / self.screen_width
        )
        self.ship.draw(self.screen, self.frametime_s, self.speed)
        self.fuel_gaige.draw(self.screen, self.ship.fuel / self.ship.ship_fuel_capacity)
        self.pilot_display.render(self.screen, self.ship.pilot_avatar, self.ship.pilot_name)
        self.txt.render(
            self.screen,
            (self.screen_width / 2, 0),
            (
                f"coordinates: ({self.ship.world_coordinates[0]:5.0f},{self.ship.world_coordinates[1]:5.0f}) "
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