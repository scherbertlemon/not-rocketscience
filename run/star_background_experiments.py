from not_rocketscience.framework import GameBase, ScrollingStars
import pygame
import numpy as np


class Stars(GameBase):

    SCREEN_SIZE = (800, 600)

    def __init__(self):
        super().__init__(self.SCREEN_SIZE)
        self.star_bg = ScrollingStars((1600, 1200), n_stars=200, spacecolor=(20, 20, 80), n_layers=10)
        self.pos = 0.5 * np.array(self.screen_size)
        self.speed = [0, 0]
        self.poss = [0.5 * np.array(self.screen_size) for _ in self.star_bg.surfaces]

    def render_scene(self):
        
        self.screen.fill((0, 0, 0, 255))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.speed[0] > -150:
            self.speed[0] -= 5
        if keys[pygame.K_RIGHT] and self.speed[0] < 150:
            self.speed[0] += 5
        if keys[pygame.K_UP] and self.speed[1] > -150:
            self.speed[1] -= 5
        if keys[pygame.K_DOWN] and self.speed[1] < 150:
            self.speed[1] += 5
        # self.star_bg.blit(self.screen, (400, 300))

        # self.logger.debug(self.speed)
        
        # pygame.draw.ellipse(self.screen, (255, 255, 0), ())

        for i, surf in enumerate(self.star_bg.surfaces):
            self.poss[i] -= self.frametime_s * ((i+1) / len(self.star_bg.surfaces)) * np.array(self.speed)
            rect = surf.get_rect()
            pos = self.poss[i] - 0.5 * np.array((rect.width, rect.height))
            self.screen.blit(surf, tuple(pos))

        # self.pos -= self.frametime_s * np.array(self.speed)

        # self.screen.blit(self.star_bg.surfaces[1], (10, 10))
        # self.screen.blit(self.star_bg.surfaces[2], (10, 10))

        
        
    
    def process_inputs(self):
        pass


if __name__ == "__main__":
    game = Stars()
    game.gameloop()