import pygame
import numpy as np
import logging
from .config import init_log


class Parameters:
    # screen size
    SCREEN_SIZE = (800, 600)

    # colors
    

    # background layers
    NUMBER_OF_BG_LAYERS = 2


class GameBase:
    
    def __init__(self, screen_size, fps=60):
        init_log()
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = fps
        self.frametime_s = 0

    @property
    def screen_width(self):
        return self.screen_size[0]

    @property
    def screen_height(self):
        return self.screen_size[1]

    def render_scene(self):
        raise NotImplementedError("needs to be implemented in subclass")

    def process_inputs(self):
        raise NotImplementedError("needs to be implemented in subclass")
    
    def gameloop(self):
        self.logger.info("Commencing game loop")
        self.running = True
        try:
            while self.running:
                self.process_inputs()
                self.render_scene()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                pygame.display.flip()
                self.frametime_s = self.clock.tick(self.fps) / 1000
        finally:
            self.logger.info(f"Exiting. Last frametime was {self.frametime_s}s")
            pygame.quit()


class ScrollingStars:

    def __init__(self, size, spacecolor=(10, 10, 30, 255), starcolor=(255, 255, 200, 255), n_layers=3, n_stars=20, star_size=2):
        self.logger = logging.getLogger("ScrollingStars")
        self.size = size
        self.space_color = spacecolor
        self.star_color = starcolor
        self.n_layers = n_layers
        self.n_stars = n_stars
        self.star_size = star_size
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
                scale_factor = 1 + i * 0.5
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
            pygame.draw.rect(surf, self.star_color, (star_coordinates[0, index], star_coordinates[1, index], self.star_size, self.star_size))

    def blit(self, screen, middle_pos):
        for surf in self.surfaces:
            rect = surf.get_rect()
            upper_right_corner = (
                middle_pos[0] - int(rect.width * 0.5),
                middle_pos[1] - int(rect.height * 0.5)
            )
            screen.blit(surf, upper_right_corner)

        




    
        