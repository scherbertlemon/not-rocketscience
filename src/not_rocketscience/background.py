import logging
import pygame
import numpy as np


class ScrollingStars:

    def __init__(self,
                 size: tuple,
                 screen_size: tuple,
                 initial_position: np.array,
                 spacecolor=(10, 10, 30, 255),
                 starcolor=(255, 255, 200, 255),
                 n_layers=3,
                 n_stars=20,
                 star_size=2):
        
        self.logger = logging.getLogger("ScrollingStars")
        self.size = size
        self.screen_size = screen_size
        self.space_color = spacecolor
        self.star_color = starcolor
        self.n_layers = n_layers
        self.n_stars = n_stars
        self.star_size = star_size
        self.layer_positions = [initial_position.copy() for _ in range(0, n_layers)]
        self._surfaces = None 

    @property
    def surfaces(self):
        if self._surfaces is None:
            self._surfaces = []
            for i in range(0, self.n_layers):
                self.logger.debug(f"Generating surface {i}")
                surf = pygame.Surface(self.size).convert_alpha()
                if i == 0:
                    surf.fill(self.space_color)
                else:
                    surf.fill(self.space_color[:3] + (0,))
                self.add_stars(surf, self.n_stars)
                scale_factor = 1 + i * .75
                self._surfaces.append(
                    pygame.transform.scale(
                        surf, 
                        (int(scale_factor * self.size[0]), int(scale_factor * self.size[1]))
                    )
                )
        return self._surfaces
        
    def add_stars(self, surf, n_stars):
        star_coordinates = np.vstack(
            (
                np.random.randint(0, self.size[0], (1, n_stars)),
                np.random.randint(0, self.size[1], (1, n_stars))
            )
        )
        for index in range(0, star_coordinates.shape[1]):
            pygame.draw.rect(
                surf,
                self.star_color,
                (star_coordinates[0, index], star_coordinates[1, index], self.star_size, self.star_size)
            )

    def blit(self, screen, dt=0, speed=np.zeros((1,2))):
        for i, surf in enumerate(self.surfaces):
            self.layer_positions[i] -= dt * (i + 1) / (self.n_layers + 1) * speed
            rect = surf.get_rect(center=tuple(self.layer_positions[i]))
            pos = self.layer_positions[i] - 0.5 * np.array((rect.width, rect.height))
            screen.blit(surf, rect)
