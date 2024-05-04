from not_rocketscience import GameBase, config, ScrollingStarBackground, LayeredScrollingStarBackrgound
import numpy as np
import pygame


class Stars(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size), fps=60)
        
        # self.star_bg = ScrollingStarBackground(
        #     (100, 100),
        #     0.5 * np.array(self.screen_size),
        #     n_stars=10,
        #     spacecolor=config.hex_to_rgb(config.space_color),
        #     starcolor=config.hex_to_rgb(config.star_color),
        # )
        self.star_bg = LayeredScrollingStarBackrgound(
            (100, 100),
            0.5 * np.array(self.screen_size),
            n_stars=10,
            spacecolor=config.hex_to_rgb(config.space_color),
            starcolor=config.hex_to_rgb(config.star_color),
            n_layers=4
        )
        
        self.pos = 0.5 * np.array(self.screen_size)
        self.accel = np.array([0, 0])
        self.speed = np.array([0, 0])
        self.damp = 0.7

    def render_scene(self):
        # self.speed = np.array((15, 10))
        self.speed = self.speed + self.frametime_s * (self.accel - self.speed * self.damp)
        self.star_bg.draw_tiles(self.screen, self.pos, self.frametime_s, self.speed)
        pygame.draw.rect(self.screen, (255, 0, 0), tuple(self.pos - 5) + (10, 10))

    def process_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed[0] -= 10
        if keys[pygame.K_RIGHT]:
            self.speed[0] += 10
        if keys[pygame.K_UP]:
            self.speed[1] -= 10
        if keys[pygame.K_DOWN]:
            self.speed[1] += 10


if __name__ == "__main__":
    game = Stars()
    game.gameloop()