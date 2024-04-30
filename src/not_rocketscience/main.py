import pygame
import numpy as np

from .framework import GameBase
from .config import config
from .background import ScrollingStars


class NotRocketScience(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size))
        
        self.star_background = ScrollingStars(
            tuple(5 * dim for dim in self.screen_size),
            0.5 * np.array(self.screen_size),
            n_stars=1000,
            spacecolor=config.hex_to_rgb(config.background["space_color"]),
            starcolor=config.hex_to_rgb(config.background["star_color"]),
            n_layers=4
        )

        self.ship_layer = pygame.Surface((100, 100)).convert_alpha()
        self.ship_layer.fill((0, 0, 0, 0))
        self.ship = pygame.draw.rect(self.ship_layer, (255, 0, 0, 255), (40, 25, 20, 50))
        self.screen.fill(config.hex_to_rgb(config.background["space_color"]))
        self.rotation = 0
        self.angle = 0
        self.thrust = 0

        self.planet_pos = np.array((900, 200))
        self.planet_color = (200, 170, 0, 255)

        self.pos = 0.5 * np.array(self.screen_size)
        self.accel = np.array([0, 0])
        self.speed = np.array([0, 0])
        self.damp = 0.2
        # self.poss = [0.5 * np.array(self.screen_size) for _ in self.star_bg.surfaces]

    def fire_color(self):
        return 255, 200, 100, 200 if self.thrust else 0
    
    def render_scene(self):
        
        self.angle += self.rotation
        angle_rad = self.angle / 180 * np.pi
        self.accel = np.matmul(
            np.array([
                [np.cos(angle_rad), np.sin(angle_rad)],
                [-np.sin(angle_rad), np.cos(angle_rad)]
            ]),
            np.array([0, -self.thrust])
        )

        # diff = 0.01 * (self.planet_pos - self.pos)
        # grav = 100 * diff / np.sqrt(np.sum(diff**2))**3
        # self.accel = self.accel + grav

        # self.logger.debug(grav)

        self.speed = self.speed + self.frametime_s * (self.accel - self.speed * self.damp)
        self.screen.fill((0, 0, 0, 255))
        self.star_background.blit(self.screen, self.frametime_s, self.speed)

        self.planet_pos = self.planet_pos - self.frametime_s * self.speed
        
        # self.logger.debug(f"angle: {self.angle}")
        pygame.draw.rect(self.ship_layer, self.fire_color(), (45, 75, 10, 15))
        rotated_ship = pygame.transform.rotate(self.ship_layer, self.angle)
        pos = rotated_ship.get_rect(center=tuple(0.5 * np.array(self.screen_size)))
        pygame.draw.ellipse(self.screen, self.planet_color , tuple(self.planet_pos) + (50, 50))
        self.screen.blit(rotated_ship, pos)

    def process_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation = 5
        elif keys[pygame.K_RIGHT]:
            self.rotation = -5
        else:
            self.rotation = 0

        if keys[pygame.K_SPACE]:
            self.thrust = 200
        else:
            self.thrust = 0