from not_rocketscience import GameBase, ScrollingStars, config
import numpy as np
import pygame


class Stars(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size))
        
        self.star_bg = ScrollingStars(
            tuple(5 * dim for dim in self.screen_size),
            0.5 * np.array(self.screen_size),
            n_stars=1000,
            spacecolor=config.hex_to_rgb(config.background["space_color"]),
            starcolor=config.hex_to_rgb(config.background["star_color"]),
            n_layers=4
        )
        
        self.pos = 0.5 * np.array(self.screen_size)
        self.accel = np.array([0, 0])
        self.speed = np.array([0, 0])
        self.damp = 0.7
        # self.poss = [0.5 * np.array(self.screen_size) for _ in self.star_bg.surfaces]

    def render_scene(self):
        
        self.speed = self.speed + self.frametime_s * (self.accel - self.speed * self.damp)
        self.screen.fill((0, 0, 0, 255))
        self.star_bg.blit(self.screen, self.frametime_s, self.speed)

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