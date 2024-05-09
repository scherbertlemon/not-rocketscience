import pygame
import numpy as np
from .config import config


class Ship:

    def __init__(self, initial_position):
        # self.layer = pygame.Surface((100, 100)).convert_alpha()
        # self.layer.fill((0, 0, 0, 0))
        # self.ship = pygame.draw.rect(self.layer, (255, 0, 0, 255), (40, 25, 20, 50))
        self.sprites = [pygame.image.load(config.asset_path / f"ship{i}.png") for i in range(5, 9)]
        self.angle = 0
        self.thrust = 0
        self.rotation = 0
        self.last_time = pygame.time.get_ticks()
        self.sprite_index = 0
        self.pos, self._coordinates = initial_position.copy(), initial_position.copy()

    @property
    def angle_rad(self):
        return self.angle / 180 * np.pi
    
    @property
    def layer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:
            self.last_time = current_time
            self.sprite_index = (self.sprite_index + 1) % 2
        return self.sprites[self.sprite_index + 2 * int(bool(self.thrust))]
    
    def apply_rotation(self):
        self.angle += self.rotation

    def calc_acceleration(self):
        return np.matmul(
            np.array([
                [np.cos(self.angle_rad), np.sin(self.angle_rad)],
                [-np.sin(self.angle_rad), np.cos(self.angle_rad)]
            ]),
            np.array([0, -self.thrust])
        )
    
    def move(self, offset):
        self._coordinates += offset

    @property
    def coordinates(self):
        return self._coordinates
    
    def draw(self, screen):
        # pygame.draw.rect(self.layer, self.fire_color, (45, 75, 10, 15))
        rotated_ship = pygame.transform.rotate(self.layer, self.angle)
        screen.blit(rotated_ship, rotated_ship.get_rect(center=self.pos))

    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation = config.ship_rotation_increment
        elif keys[pygame.K_RIGHT]:
            self.rotation = -config.ship_rotation_increment
        else:
            self.rotation = 0

        if keys[pygame.K_x]:
            self.thrust = config.ship_thrust
        else:
            self.thrust = 0
