"""
Classes for managing the spaceship movement, animation and rotation
"""
import logging
import re
import pygame
import numpy as np
from pprint import pformat
from .config import config


class Ship:
    """
    Main class that holds all ship properties
    """
    def __init__(
        self,
        initial_position,
        asset_path=None,
        sprite_name_pattern=r"ship_cd_\d\.png",
        pilot_name="Cptn Default",
        ship_animation_frames=2,
        ship_thrust=400,
        ship_rotation_speed=270,
        ship_movement_damping=0.1,
        ship_fuel_consumption=1,
        ship_fuel_capacity=100,
        ship_fuel_regeneration=2
    ):
        self.logger = logging.getLogger("Ship")
        if asset_path is None:
            asset_path = config.asset_path / "ships"

        self.sprite_filenames = sorted([
            file
            for file in asset_path.glob("*.png") if re.match(sprite_name_pattern, file.name)
        ])
        self.logger.info("found ship sprites:\n%s", pformat([f.name for f in self.sprite_filenames]))

        self.pilot_name = pilot_name
        self.ship_animation_frames =  ship_animation_frames
        self.ship_thrust = ship_thrust
        self.ship_rotation_speed = ship_rotation_speed
        self.ship_movement_damping = ship_movement_damping
        self.ship_fuel_consumption = ship_fuel_consumption
        self.ship_fuel_capacity = ship_fuel_capacity
        self.ship_fuel_regeneration = ship_fuel_regeneration

        self.sprites = [pygame.image.load(filename) for filename in self.sprite_filenames]

        self._angle = 0
        self._thrust = 0
        self._rotation_speed = 0
        self._last_time = pygame.time.get_ticks()
        self._sprite_index = 0
        self._fuel = self.ship_fuel_capacity
        self._screen_coordinates, self._world_coordinates = initial_position.copy(), initial_position.copy()

    @property
    def angle_rad(self):
        return self._angle / 180 * np.pi

    @property
    def layer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self._last_time >= 1000:
            self._last_time = current_time
            self._sprite_index = (self._sprite_index + 1) % self.ship_animation_frames
        return self.sprites[self._sprite_index + self.ship_animation_frames * int(bool(self.thrust))]

    def apply_rotation(self, dt):
        self._angle += dt * self._rotation_speed

    def calc_acceleration(self):
        """
        Result of rotation matrix with `self.angle_rad` and thrust vector
        """
        return np.array([-np.sin(self.angle_rad) * self._thrust, -np.cos(self.angle_rad) * self.thrust])

    def move(self, offset):
        self._world_coordinates += offset

    def consume_fuel(self, dt):
        if self._thrust and self.fuel >= 0:
            self._fuel -= self.ship_fuel_consumption * dt

    def regenerate_fuel(self, dt, multiplier):
        if self._fuel <= self.ship_fuel_capacity:
            self._fuel += dt * multiplier * self.ship_fuel_regeneration

    @property
    def fuel(self):
        return self._fuel
    
    @property
    def thrust(self):
        return self._thrust if self.fuel >= 0 else 0

    @property
    def world_coordinates(self):
        return self._world_coordinates

    def draw(self, screen, dt, speed):
        self.consume_fuel(dt)
        self.apply_rotation(dt)
        self.move(dt * speed)
        rotated_ship = pygame.transform.rotate(self.layer, self._angle)
        screen.blit(rotated_ship, rotated_ship.get_rect(center=self._screen_coordinates))

    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._rotation_speed = self.ship_rotation_speed
        elif keys[pygame.K_RIGHT]:
            self._rotation_speed = -self.ship_rotation_speed
        else:
            self._rotation_speed = 0

        if keys[pygame.K_x]:
            self._thrust = self.ship_thrust
        else:
            self._thrust = 0

        if keys[pygame.K_r]:
            self._fuel = self.ship_fuel_capacity
