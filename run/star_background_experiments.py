"""
Demonstrate the scrolling star background
"""
import numpy as np
import pygame
from not_rocketscience import GameBase, config, ScrollingStarBackground, \
    LayeredScrollingStarBackground


class Stars(GameBase):

    def __init__(self):
        super().__init__(config.screen_size, vsync=True)

        self.star_bg = ScrollingStarBackground(
            (100, 100),
            0.5 * np.array(self.screen_size),
            n_stars=10,
            space_color=config.colors.space,
            star_color=config.colors.stars,
        )
        # self.star_bg = LayeredScrollingStarBackground(
        #     (100, 100),
        #     0.5 * np.array(self.screen_size),
        #     n_stars=5,
        #     space_color=config.colors.space,
        #     star_color=config.colors.stars,
        #     n_layers=3
        # )

        self.pos = 0.5 * np.array(self.screen_size)
        self.accel = np.array([0, 0])
        self.accel_amount = 800
        self.speed = np.array([0, 0])
        self.damp = 0.7

    def render_scene(self):

        self.speed = self.speed + self.frametime_s * (self.accel - self.speed * self.damp)
        self.star_bg.draw_tiles(self.screen, self.pos, self.frametime_s, self.speed)
        pygame.draw.rect(self.screen, config.colors.ship_red, tuple(self.pos - 5) + (10, 10))

    def process_inputs(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.accel_amount
        if keys[pygame.K_RIGHT]:
            dx = self.accel_amount
        if keys[pygame.K_UP]:
            dy = -self.accel_amount
        if keys[pygame.K_DOWN]:
            dy = self.accel_amount

        self.accel = np.array([dx, dy])


if __name__ == "__main__":
    game = Stars()
    game.gameloop()
